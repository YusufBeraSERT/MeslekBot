import discord
from discord.ext import commands
from discord.ui import Select, View
from google import genai
import json
import os

# --- VERI TABANI FONKSIYONLARI ---
def load_careers_database():
    if os.path.exists("careers_db.json"):
        with open("careers_db.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# --- YAPAY ZEKA VE BOT AYARLARI ---
# Yapay zeka istemcisini baslatiyoruz. 
# Sisteminizin ortam degiskenlerinde GEMINI_API_KEY tanimli olmalidir.
ai_client = genai.Client()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- UI BILESENLERI (Menuler) ---
class CareerSelectionMenu(Select):
    def __init__(self, database_data):
        options = []
        for key, data in database_data.items():
            options.append(discord.SelectOption(
                label=data["title"], 
                value=key, 
                description=f"{data['title']} alanini inceleyin."
            ))
        
        super().__init__(
            placeholder="Incelemek istediginiz kariyer yolunu seciniz...", 
            min_values=1, 
            max_values=1, 
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        database = load_careers_database()
        selected_key = self.values[0]
        career_data = database.get(selected_key)

        if career_data:
            embed = discord.Embed(
                title=career_data["title"],
                description=career_data["description"],
                color=discord.Color.blue()
            )
            embed.add_field(name="Gereken Temel Yetenekler", value=", ".join(career_data["skills"]), inline=False)
            
            steps_text = "\n".join([f"{index+1}. {step}" for index, step in enumerate(career_data["steps"])])
            embed.add_field(name="Tavsiye Edilen Yol Haritasi", value=steps_text, inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("Meslek bulunamadi.", ephemeral=True)

class CareerMenuView(View):
    def __init__(self, database_data):
        super().__init__()
        self.add_item(CareerSelectionMenu(database_data))


# --- BOT ETKILESIM KOMUTLARI (Arttirilmis Komut Seti) ---

@bot.event
async def on_ready():
    print(f"Bot aktif: {bot.user.name}")

# Komut 1: Menu Listeleme
@bot.command(name="kariyer")
async def kariyer_menusu(ctx):
    """Butonlu ve menulu ana kariyer listesini acar."""
    database = load_careers_database()
    if not database:
        await ctx.send("Kariyer veri tabani yuklenemedi.")
        return
    view = CareerMenuView(database)
    await ctx.send("Kariyer seceneklerini listelemek ve detaylarini ogrenmek icin asagidaki menuyu kullanabilirsiniz:", view=view)

# Komut 2: Veri Tabaninda Hizli Arama
@bot.command(name="ara")
async def kariyer_ara(ctx, *, aranan_kelime: str):
    """Veri tabaninda eslesen meslekleri hizlica listeler."""
    database = load_careers_database()
    found = False
    
    for key, data in database.items():
        if aranan_kelime.lower() in data["title"].lower() or aranan_kelime.lower() in key:
            embed = discord.Embed(
                title=f"Arama Sonucu: {data['title']}",
                description=data["description"],
                color=discord.Color.dark_green()
            )
            embed.add_field(name="Gereken Yetenekler", value=", ".join(data["skills"]), inline=False)
            steps_text = "\n".join([f"- {step}" for step in data["steps"]])
            embed.add_field(name="Yol Haritasi", value=steps_text, inline=False)
            await ctx.send(embed=embed)
            found = True
            break
            
    if not found:
        await ctx.send(f"Veri tabaninda '{aranan_kelime}' ile ilgili sonuc bulunamadi. Yapay zekaya sormak icin '!sor' komutunu kullanabilirsiniz.")

# Komut 3: YAPAY ZEKA ENTEGRASYONU (Serbest Danismanlik)
@bot.command(name="sor")
async def yapay_zeka_sor(ctx, *, kullanici_sorusu: str):
    """Kullanicinin kariyer sorularini dogrudan Yapay Zeka (AI) ile yanitlar."""
    # Kullaniciya botun dusundugunu belirtmek icin gecici bir mesaj gonderiyoruz
    bekleme_mesaji = await ctx.send("Kariyer danismani yapay zeka cevabi hazirliyor, lutfen bekleyiniz...")

    try:
        # Yapay zekaya rol tanimi (System Instruction) vererek tam bir kariyer danismani gibi davranmasini sagliyoruz
        prompt = (
            "Sen genc girisimciler ve kariyer degistirmek isteyenler icin profesyonel bir kariyer danismanisin. "
            "Gelen soruya hicbir emoji kullanmadan, net, motive edici ve anlasilir bir dille cevap ver. "
            "Soru su: " + kullanici_sorusu
        )

        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        # Gelen cevabi temiz bir kutu (Embed) icinde gosteriyoruz
        embed = discord.Embed(
            title="Yapay Zeka Danismanlik Yaniti",
            description=response.text,
            color=discord.Color.purple()
        )
        
        await bekleme_mesaji.delete()
        await ctx.send(embed=embed)

    except Exception as e:
        await bekleme_mesaji.delete()
        await ctx.send("Yapay zeka servisine ulasilirken bir hata olustu. Lutfen daha sonra tekrar deneyiniz.")

# Komut 4: Yardim / Kilavuz Komutu
@bot.command(name="yardim")
async def yardim_komutu(ctx):
    """Botun tum islevlerini kullaniciya acıklar."""
    embed = discord.Embed(
        title="Kariyer Botu Kullanim Kilavuzu",
        description="Bot ile etkilesime gecmek icin asagidaki komutlari kullanabilirsiniz:",
        color=discord.Color.orange()
    )
    embed.add_field(name="!kariyer", value="Butonlu ve secim menulu interaktif meslek listesini gosterir.", inline=False)
    embed.add_field(name="!ara [meslek adi]", value="Veri tabaninda kayitli meslekler arasinda hizli arama yapar.", inline=False)
    embed.add_field(name="!sor [sorunuz]", value="Kariyer, meslek secimi veya gelecek planlari hakkinda YAPAY ZEKAYA serbestce soru sormanizi saglar.", inline=False)
    
    await ctx.send(embed=embed)


bot.run("MTUxNzU3NzU4OTE2MDY3NzQ0Nw.GCY9zE.dsS1NCSCp-Cw9JZQzsvZ_lAoWYkCcqpGQ0VA5Q")
