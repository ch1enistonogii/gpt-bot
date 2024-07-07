import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

class ChatGPTClient(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_gpt3_prompt = None
        self.last_gpt3_response = None
        self.user_1_last_message = None
        self.user_1_last_response = None
        self.user_2_last_message = None
        self.user_2_last_response = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')
            await channel.send("https://images-ext-1.discordapp.net/external/HcfEIxo_k3CtpeP8fVQOImxievqQC_dfCZ2MtTtM1BE/https/media.tenor.com/w78adlWSxnkAAAPo/why-recycle-bin.mp4")

    def generate_gpt3_response(self, prompt, history):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f'Ты чат бот, ответ на русском, не более 150 символов. {history}'},
                {"role": "user", "content": f'Текущий запрос: {prompt}'},
            ],
        )
        return response.choices[0].message['content']

    def generate_gpt4_response(self, prompt, history):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f'Ответ на русском. {history}'},
                {"role": "user", "content": f'Текущий запрос: {prompt}; Текущий ответ: '},
            ],
        )
        return response.choices[0].message['content']

    def split_message(self, message, max_length=2000):
        return [message[i:i+max_length] for i in range(0, len(message), max_length)]

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message):
            if message.author.id == 984097688167546881:
                user_prompt = message.content.replace(self.bot.user.mention, '').strip()
                user_history = f"Предыдущий запрос: {self.user_1_last_message}; Предыдущий ответ: {self.user_1_last_response};"
                gpt_response = self.generate_gpt4_response(user_prompt, user_history)
                response_chunks = self.split_message(gpt_response)
                for chunk in response_chunks:
                    await message.channel.send(f'{chunk}')
                print(f"Admin User {message.author} used the command. Message: {user_prompt}")
                self.user_1_last_message = user_prompt
                self.user_1_last_response = gpt_response

            elif message.author.id == 350215622333825035:
                user_prompt = message.content.replace(self.bot.user.mention, '').strip()
                user_history = f"Предыдущий запрос: {self.user_2_last_message} Предыдущий ответ: {self.user_2_last_response}"
                gpt_response = self.generate_gpt4_response(user_prompt, user_history)
                response_chunks = self.split_message(gpt_response)
                for chunk in response_chunks:
                    await message.channel.send(f'{chunk}')
                print(f"Admin User {message.author} used the command. Message: {user_prompt}")
                self.user_2_last_message = user_prompt
                self.user_2_last_response = gpt_response

            elif message.channel.id == 1152933705581609030:
                user_prompt = message.content.replace(self.bot.user.mention, '').strip()
                user_history = f"Предыдущий запрос: {self.last_gpt3_prompt} Предыдущий ответ: {self.last_gpt3_response}"
                gpt_response = self.generate_gpt3_response(user_prompt, user_history)
                await message.reply(f'{gpt_response}')
                print(f"User {message.author} used the command. Message: {user_prompt}")
                self.last_gpt3_prompt = user_prompt
                self.last_gpt3_response = gpt_response

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.add_cog(ChatGPTClient(self))
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print("\n"
          " ___ ___   _____ ___   _   __  __ \n"
          "| _ \ _ \ |_   _| __| /_\ |  \/  |\n"
          "|  _/   /   | | | _| / _ \| |\/| |\n"
          "|_| |_|_\   |_| |___/_/ \_\_|  |_|\n")

    print()
    print(" - Информация о боте - ")
    print("Имя бота: {0.user}".format(bot))
    print(f"ID бота: {bot.user.id}")
    print(f"Пинг во время запуска: {round(bot.latency * 1000)} мс")

bot.run(DISCORD_TOKEN)
