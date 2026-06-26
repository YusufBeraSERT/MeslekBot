import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput
from google import genai
from google.genai import types
import io

# --- YAPAY ZEKA VE CORE PROTOKOL KURULUMU ---
ai_client = genai.Client(api_key="API KEY GİR!")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 🛰️ SİBER KARİYER PENCERELERİ (MODALS) ---

class SoruModal(Modal, title="⚡ CORE AI: Hızlı Soru-Cevap"):
    input_field = TextInput(label="Sektörel / Teknolojik Sorunuz", style=discord.TextStyle.paragraph, placeholder="Örn: 5 yıl sonra hangi yazılım dili tahtı ele geçirecek?", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        res = ai_client.models.generate_content(model='gemini-2.5-flash', contents="Soruya sadece 3 kisa cumleyle, cok net ve oz bir vizyoner cevap ver. Asla emoji kullanma: " + self.input_field.value)
        await interaction.followup.send(embed=discord.Embed(title="💾 ANALİZ TAMAMLANDI", description=res.text[:2000], color=discord.Color.dark_purple()), ephemeral=True)

class CizimModal(Modal, title="🌀 VISION ARCHITECT: Geleceği Modelle"):
    input_field = TextInput(label="Hayalindeki Ofis / Geleceğin Mesleği", style=discord.TextStyle.paragraph, placeholder="Örn: 2050 yılında bir kuantum siber güvenlik merkezinin mimarisi", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            result = ai_client.models.generate_images(model='imagen-3.0-generate-002', prompt=self.input_field.value, config=types.GenerateImagesConfig(number_of_images=1, output_mime_type="image/jpeg"))
            image_bytes = io.BytesIO(result.generated_images[0].image.image_bytes)
            await interaction.followup.send(content=f"🛰️ **Gelecek Tasarımı Çıktısı Alındı:** {self.input_field.value}", file=discord.File(image_bytes, filename="vizyon.jpg"), ephemeral=True)
        except:
            await interaction.followup.send("⚠️ Görüntü işleme istasyonunda hata oluştu.", ephemeral=True)

class ProfilModal(Modal, title="🧬 PROFILE SCANNER: Kariyer Rotası"):
    input_field = TextInput(label="Bildiğin Teknolojiler / Kişilik Özelliklerin", style=discord.TextStyle.paragraph, placeholder="Örn: Python biliyorum, liderlik yönüm güçlü ama matematikten nefret ederim.", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        res = ai_client.models.generate_content(model='gemini-2.5-flash', contents=f"Bu profile en uygun 2 meslegi su formatta cok kisa yaz: Meslek 1: Aciklama. Meslek 2: Aciklama. Asla emoji kullanma: {self.input_field.value}")
        await interaction.followup.send(embed=discord.Embed(title="📊 ALGORİTMİK TAVSİYE RAPORU", description=res.text[:2000], color=discord.Color.blue()), ephemeral=True)

class MulakatModal(Modal, title="🧠 INTERVIEW BOT: Mülakat Simülatörü"):
    input_field = TextInput(label="Hedeflediğin Meslek Nedir?", style=discord.TextStyle.short, placeholder="Örn: Frontend Developer, Siber Güvenlik Uzmanı...", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        res = ai_client.models.generate_content(model='gemini-2.5-flash', contents=f"Bu meslek icin teknik mülakatlarda sorulan, adayi en cok zorlayan tek bir kritik soru yaz. Emoji kullanma: {self.input_field.value}")
        await interaction.followup.send(embed=discord.Embed(title="🎯 KRİTİK MÜLAKAT SORUNUZ", description=res.text[:2000], color=discord.Color.red()), ephemeral=True)

class GirişimModal(Modal, title="💡 VENTURE CAP: Girişimcilik Fikir Kutusu"):
    input_field = TextInput(label="İlgi Duyduğun Sektör Nedir?", style=discord.TextStyle.short, placeholder="Örn: Yapay zeka, tarım, oyun sektörü, e-ticaret...", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        res = ai_client.models.generate_content(model='gemini-2.5-flash', contents=f"Bu sektorde su an dunyada acik olan, para kazandirabilecek cok kisa bir girisimcilik fikri ver. Asla emoji kullanma: {self.input_field.value}")
        await interaction.followup.send(embed=discord.Embed(title="🚀 STARTUP KONSEPTİ", description=res.text[:2000], color=discord.Color.gold()), ephemeral=True)

class CvModal(Modal, title="📝 CV DEFENDER: Özgeçmiş Hata Avcısı"):
    input_field = TextInput(label="CV'ne Yazdığın Özet Cümleyi Buraya Yapıştır", style=discord.TextStyle.paragraph, placeholder="Örn: Kendini geliştirmeye açık, takım çalışmasına yatkın...", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        res = ai_client.models.generate_content(model='gemini-2.5-flash', contents=f"Bu CV ozet cumlesindeki klise hatalari acikla ve daha profesyonel durması icin cok kisa tek bir alternatif cumle yaz. Emoji kullanma: {self.input_field.value}")
        await interaction.followup.send(embed=discord.Embed(title="🛠️ CV DÜZELTME ÖNERİSİ", description=res.text[:2000], color=discord.Color.orange()), ephemeral=True)

class TrendModal(Modal, title="📉 TREND ANALYST: Sektörün Geleceği"):
    input_field = TextInput(label="Hangi Mesleğin Geleceğini Merak Ediyorsun?", style=discord.TextStyle.short, placeholder="Örn: Grafik Tasarım, Avukatlık, Makine Mühendisliği...", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        res = ai_client.models.generate_content(model='gemini-2.5-flash', contents=f"Bu meslegin onumuzdeki 10 yilda yok olma riski yuzde kactir ve sirketler artik ne talep edecek? Cok kisa yaz, emoji kullanma: {self.input_field.value}")
        await interaction.followup.send(embed=discord.Embed(title="🔮 MESLEKİ GELECEK PROJEKSİYONU", description=res.text[:2000], color=discord.Color.teal()), ephemeral=True)

# --- 🛰️ SİBER KARİYER TERMİNALİ (Arayüz Paneli) ---
class CyberCareerPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

    # 1. Row: Temel AI Fonksiyonları
    @discord.ui.button(label="▪️ CORE AI [SORU]", style=discord.ButtonStyle.secondary, row=0)
    async def b_sor(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SoruModal())

    @discord.ui.button(label="▪️ VISION INFRA [MİMARİ ÇİZ]", style=discord.ButtonStyle.success, row=0)
    async def b_ciz(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CizimModal())

    # 2. Row: Profiler ve Simülasyon
    @discord.ui.button(label="▪️ PROFILE SCANNER [ROTA]", style=discord.ButtonStyle.primary, row=1)
    async def b_analiz(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ProfilModal())

    @discord.ui.button(label="▪️ INTERVIEW PROT [MÜLAKAT]", style=discord.ButtonStyle.danger, row=1)
    async def b_mulakat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(MulakatModal())

    # 3. Row: Girişimcilik ve Gelişim Bölümü
    @discord.ui.button(label="▪️ VENTURE CAPITAL [GİRİŞİM]", style=discord.ButtonStyle.secondary, row=2)
    async def b_girisim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(GirişimModal())

    @discord.ui.button(label="▪️ CV ANALYST [CV KONTROL]", style=discord.ButtonStyle.secondary, row=2)
    async def b_cv(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CvModal())

    # 4. Row: İstihbarat ve Küresel Trendler
    @discord.ui.button(label="▪️ METRIC FORECAST [TRENDLER]", style=discord.ButtonStyle.secondary, row=3)
    async def b_trend(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TrendModal())

    @discord.ui.button(label="▪️ STAGE PROTOCOL [KILAVUZ]", style=discord.ButtonStyle.secondary, row=3)
    async def b_staj(self, interaction: discord.Interaction, button: discord.ui.Button):
        rehber = "1. Sektör liderlerini LinkedIn üzerinden takip edip takibe alın.\n2. Global açık kaynak kodlu (Open Source) projelere katkı verin.\n3. Teorik ezber yerine her hafta canlı çalışan minimal bir servis ayağa kaldırın."
        await interaction.response.send_message(embed=discord.Embed(title="⚙️ GLOBAL GELİŞİM PROTOKOLÜ", description=rehber, color=discord.Color.dark_blue()), ephemeral=True)

# --- SİSTEM TETİKLEYİCİ ---
@bot.event
async def on_ready():
    print(f"🤖 KÜRESEL KARİYER TERMİNALİ ÇALIŞIYOR: {bot.user.name}")

@bot.command(name="panel")
async def panel_gonder(ctx):
    embed = discord.Embed(
        title="🛰️ QUANTUM CAREER MANAGEMENT CENTRAL INTERFACE",
        description=(
            "Geleneksel eğitim kalıpları ve düz komut sistemleri sonlandırılmıştır.\n"
            "Yeni nesil endüstriyel dönüşüm, yapay zeka optimizasyonları ve klan içi kariyer "
            "yapılandırması için aşağıdaki şifreli alt terminalleri kullanın.\n\n"
            "**[Sistem Durumu: Çekirdek Aktif | Yapay Zeka Entegre]**"
        ),
        color=discord.Color.dark_grey()
    )
    embed.set_footer(text="Veri tabanı anlık güncellenir. Yapılan tüm sorgular kullanıcı paneline özel ve gizlidir.")
    await ctx.send(embed=embed, view=CyberCareerPanel())

bot.run("TOKEN GİR!")
