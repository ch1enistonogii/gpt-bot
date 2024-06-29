import discord
from discord.ext import commands
from discord import app_commands
import openai

DISCORD_TOKEN = 'MTI1MTU3NDk0MzU5MDkxMjA1Mg.GOkkvT.GbGafy_TvTNN7NmGIci9-ltjbCn3g3rG3EDU8Q'
OPENAI_API_KEY = 'sk-proj-UoBGyodRupARhnJM2HXuT3BlbkFJ22Xh9r0GOteIlAUhJUwp'

openai.api_key = OPENAI_API_KEY

class ChatGPTClient(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def generate_response(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": 'Тебя зовут Вячеслава, тебе 19 лет, пошленькая. Поддердивай диалог как девушка, не как бот'},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message['content']

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.channel.id == 1152933705581609030:
            if self.bot.user.mentioned_in(message):
                user_prompt = message.content.replace(self.bot.user.mention, '').strip()
                gpt_response = self.generate_response(user_prompt)
                await message.reply(f"{gpt_response}")

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.add_cog(ChatGPTClient(self))
        await bot.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.run(DISCORD_TOKEN)