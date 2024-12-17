import discord
from discord import app_commands
from discord.ext import commands
from googletrans import Translator
import asyncio

# Language options with flags
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
    "hi": "🇮🇳 Hindi" 
}

class LanguageSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label=lang_name.split(" ")[1],
                value=lang_code,
                emoji=lang_name.split(" ")[0],
                description=f"Set your language to {lang_name.split(' ')[1]}"
            ) for lang_code, lang_name in LANGUAGES.items()
        ]
        super().__init__(
            placeholder="Select your language",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        lang_code = self.values[0]
        self.bot.user_languages[str(interaction.user.id)] = lang_code
        await interaction.response.send_message(
            f"✅ Your language has been set to: {LANGUAGES[lang_code]}",
            ephemeral=True
        )

class LanguageView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(LanguageSelect(bot))

class TranslatorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="language", description="Select your preferred language for translations")
    async def language(self, interaction: discord.Interaction):
        """Select your preferred language for translations"""
        await interaction.response.send_message(
            "Select your preferred language:",
            view=LanguageView(self.bot),
            ephemeral=True
        )

class TranslatorBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)
        self.translator = Translator()
        self.user_languages = {}

    async def setup_hook(self):
        print("Setting up commands...")
        
        # Create context menu command for translation
        @self.tree.context_menu(name='Translate Message')
        async def translate_message(interaction: discord.Interaction, message: discord.Message):
            await self.handle_translation(interaction, message)

        # Add the cog with slash commands
        await self.add_cog(TranslatorCog(self))

        try:
            print("Syncing commands...")
            await self.tree.sync()
            print("Commands synced successfully!")
        except Exception as e:
            print(f"Error during sync: {e}")

    async def handle_translation(self, interaction: discord.Interaction, message: discord.Message):
        user_id = str(interaction.user.id)
        if user_id not in self.user_languages:
            await interaction.response.send_message(
                "⚠️ Please set your language first using /language",
                ephemeral=True
            )
            return

        target_lang = self.user_languages[user_id]
        try:
            translation = self.translator.translate(
                message.content,
                dest=target_lang
            )
            
            embed = discord.Embed(
                title="🔄 Translation",
                description=translation.text,
                color=0x3498db
            )
            embed.set_footer(text=f"{translation.src} → {target_lang}")
            
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Translation error: {str(e)}",
                ephemeral=True
            )

# Bot setup and launch
bot = TranslatorBot()

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user.name}')
    print("Bot is ready! Use /language to set your preferred language.")
    print(f"Invite URL: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=2048&scope=bot%20applications.commands")

# Replace with your Discord token
TOKEN = 'YOUR_TOKEN_HERE'

if __name__ == '__main__':
    bot.run(TOKEN)
