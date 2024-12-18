import discord
from discord import app_commands, Webhook
from discord.ext import commands
from googletrans import Translator
import asyncio

LANGUAGES = {
    "en": "🇺🇸 English",
    "fr": "🇫🇷 French",
    "es": "🇪🇸 Spanish",
    "de": "🇩🇪 German",
    "it": "🇮🇹 Italian",
    "pt": "🇵🇹 Portuguese",
    "ru": "🇷🇺 Russian",
    "ja": "🇯🇵 Japanese",
    "ko": "🇰🇷 Korean",
    "zh": "🇨🇳 Chinese",
    "hi": "🇮🇳 Hindi",
    "ar": "🇸🇦 Arabic"
}

class UserSettings:
    def __init__(self):
        self.target_lang = None
        self.output_lang = None
        self.auto_translate = False

    def is_ready(self):
        return all([self.target_lang, self.output_lang, self.auto_translate])

class LanguageSelect(discord.ui.Select):
    def __init__(self, bot, setting_type, placeholder):
        self.bot = bot
        self.setting_type = setting_type
        options = [
            discord.SelectOption(
                label=lang_name.split(" ")[1],
                value=lang_code,
                emoji=lang_name.split(" ")[0]
            ) for lang_code, lang_name in LANGUAGES.items()
        ]
        super().__init__(placeholder=placeholder, options=options)

    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        if user_id not in self.bot.user_settings:
            self.bot.user_settings[user_id] = UserSettings()

        settings = self.bot.user_settings[user_id]
        if self.setting_type == "target":
            settings.target_lang = self.values[0]
        else:
            settings.output_lang = self.values[0]

        content = "Current Settings:\n"
        content += f"• Input Language: {LANGUAGES.get(settings.target_lang, 'Not set')}\n"
        content += f"• Output Language: {LANGUAGES.get(settings.output_lang, 'Not set')}\n"
        content += f"• Auto-Translation: {'ON' if settings.auto_translate else 'OFF'}"

        await interaction.response.edit_message(content=content, view=self.view)

class AutoTranslateButton(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(
            style=discord.ButtonStyle.danger,
            label="Auto-Translation: OFF"
        )
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        if user_id not in self.bot.user_settings:
            self.bot.user_settings[user_id] = UserSettings()

        settings = self.bot.user_settings[user_id]
        settings.auto_translate = not settings.auto_translate
        
        self.label = f"Auto-Translation: {'ON' if settings.auto_translate else 'OFF'}"
        self.style = discord.ButtonStyle.success if settings.auto_translate else discord.ButtonStyle.danger

        content = "Current Settings:\n"
        content += f"• Input Language: {LANGUAGES.get(settings.target_lang, 'Not set')}\n"
        content += f"• Output Language: {LANGUAGES.get(settings.output_lang, 'Not set')}\n"
        content += f"• Auto-Translation: {'ON' if settings.auto_translate else 'OFF'}"

        await interaction.response.edit_message(content=content, view=self.view)

class SettingsView(discord.ui.View):
    def __init__(self, bot, user_id):
        super().__init__()
        self.bot = bot
        self.user_id = user_id
        self.add_item(LanguageSelect(bot, "target", "Select input language"))
        self.add_item(LanguageSelect(bot, "output", "Select output language"))
        self.add_item(AutoTranslateButton(bot))

class TranslatorBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)
        self.translator = Translator()
        self.user_settings = {}

    async def setup_hook(self):
        @self.tree.command(name="settings", description="Configure your translation settings")
        async def settings(interaction: discord.Interaction):
            user_id = str(interaction.user.id)
            if user_id not in self.user_settings:
                self.user_settings[user_id] = UserSettings()
            
            view = SettingsView(self, user_id)
            settings = self.user_settings[user_id]
            
            content = "Configure your translation settings:"
            if settings.target_lang or settings.output_lang:
                content = "Current Settings:\n"
                content += f"• Input Language: {LANGUAGES.get(settings.target_lang, 'Not set')}\n"
                content += f"• Output Language: {LANGUAGES.get(settings.output_lang, 'Not set')}\n"
                content += f"• Auto-Translation: {'ON' if settings.auto_translate else 'OFF'}"
            
            await interaction.response.send_message(content=content, view=view, ephemeral=True)

        @self.tree.context_menu(name='Translate Message')
        async def translate_message(interaction: discord.Interaction, message: discord.Message):
            user_id = str(interaction.user.id)
            if user_id not in self.user_settings:
                await interaction.response.send_message(
                    "⚠️ Please set your language first using /settings",
                    ephemeral=True
                )
                return

            settings = self.user_settings[user_id]
            if not settings.target_lang:
                await interaction.response.send_message(
                    "⚠️ Please set your target language using /settings",
                    ephemeral=True
                )
                return

            try:
                translation = self.translator.translate(
                    message.content,
                    dest=settings.target_lang
                )
                
                embed = discord.Embed(
                    title="🔄 Translation",
                    description=translation.text,
                    color=0x3498db
                )
                embed.set_footer(text=f"{translation.src} → {settings.target_lang}")
                
                await interaction.response.send_message(
                    embed=embed,
                    ephemeral=True
                )
                
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ Translation error: {str(e)}",
                    ephemeral=True
                )

        await self.tree.sync()
        print("Commands synchronized!")

    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        if user_id not in self.user_settings:
            return

        settings = self.user_settings[user_id]
        if not settings.is_ready():
            return

        try:
            detected = self.translator.detect(message.content)
            if detected.lang == settings.target_lang:
                # Traduire d'abord
                translation = await asyncio.to_thread(
                    self.translator.translate,
                    message.content,
                    dest=settings.output_lang
                )

                webhook = await message.channel.create_webhook(name="TranslatorBot")
                try:
                    await message.delete()
                    
                    await webhook.send(
                        content=translation.text,
                        username=message.author.display_name,
                        avatar_url=message.author.display_avatar.url
                    )
                finally:
                    await webhook.delete()

        except Exception as e:
            print(f"Translation error: {e}")

bot = TranslatorBot()

TOKEN = 'YOUR_TOKEN_HERE'

if __name__ == '__main__':
    bot.run(TOKEN)
