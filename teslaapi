import streamlit as st
import requests
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Tesla Live Lyrics",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 1. FULL LYRICS DATABASE (SANSKRIT & WESTERN ONLY) ---
LYRICS_DATABASE = {
    
    # ==========================================
    # SANSKRIT / DEVOTIONAL (Original + English Translation)
    # ==========================================
    
    "ganesh mantra pushpanjali": """
    [00:00] ॐ यज्ञेन यज्ञमयजन्त देवाः
    [00:00] Om Yajnena Yajnam-Ayajanta Devaah
    [00:05] The Gods worshiped the Supreme Creator through sacrifice.
    
    [00:10] तानि धर्माणि प्रथमान्यासन्
    [00:10] Taani Dharmaani Prathamaanya-Aasan
    [00:15] These were the first principles of Dharma (righteousness).
    
    [00:20] ते ह नाकं महिमानः सचन्त
    [00:20] Te Ha Naakam Mahimaanaha Sachanta
    [00:25] Those great ones attain the highest heaven...
    
    [00:30] यत्र पूर्वे साध्याः सन्ति देवाः
    [00:30] Yatra Poorve Saadhyaaha Santi Devaaha
    [00:35] Where the ancient celestial beings and Gods reside.
    
    [00:40] ॐ राजाधिराजाय प्रसह्य साहिने
    [00:40] Om Raajaadhiraajaaya Prasahya Saahine
    [00:45] We offer our salutations to the King of Kings, the victorious Lord.
    
    [00:50] नमो वयं वैश्रवणाय कुर्महे
    [00:50] Namo Vayam Vaishravanaaya Kurmahe
    [00:55] We bow to Vaishravana (the Lord of Wealth).
    
    [01:00] स मे कामान् काम कामाय मह्यम्
    [01:00] Sa Me Kaamaan Kaama Kaamaaya Mahyam
    [01:05] May He fulfill all my righteous desires.
    
    [01:10] कामेश्वरो वैश्रवणो ददातु
    [01:10] Kaameshvaro Vaishravano Dadaatu
    [01:15] May the Lord of Desires, Vaishravana, grant them to me.
    
    [01:20] कुबेराय वैश्रवणाय महाराजाय नमः
    [01:20] Kuberaaya Vaishravanaaya Mahaaraajaaya Namaha
    [01:25] Salutations to Lord Kubera, the Great King.
    """,

    "sukhkarta dukhharta": """
    [00:00] सुखकर्ता दुखहर्ता, वार्ता विघ्नाची
    [00:00] Sukhkarta Dukhharta, Varta Vighnachi
    [00:05] O Lord who provides joy, takes away sorrow, and removes all obstacles in life.
    
    [00:10] नुरवी पूर्वी प्रेम कृपा जयाची
    [00:10] Nurvi Purvi Prem Krupa Jayachi
    [00:15] Who spreads love and compassion everywhere as His blessing.
    
    [00:20] सर्वांगी सुन्दर उटी शेंदुराची
    [00:20] Sarvangi Sundar Uti Shendurachi
    [00:25] Whose entire lovely body is smeared with saffron-colored paste.
    
    [00:30] कंठी झलके माल मुक्ताफलांची
    [00:30] Kanti Jhalke Mal Mukataphalaanchi
    [00:35] Around whose neck hangs a beautiful necklace of pearls.
    
    [00:40] जय देव जय देव, जय मंगल मूर्ती
    [00:40] Jaidev Jaidev Jai Mangal Murti
    [00:45] Hail the God, hail the God, hail the auspicious idol!
    
    [00:50] दर्शनमात्रे मनःकमाना पुर्ती
    [00:50] Darshan Maatre Man: Kaamna Phurti
    [00:55] All our wishes are fulfilled simply by looking at Your idol.
    
    [01:00] रत्नखचिता फरा तुझ गौरीकुमारा
    [01:00] Ratnakhachit Phara Tujh Gaurikumra
    [01:05] Offering You a jewel-studded seat, O Son of Gauri.
    
    [01:10] चंदनाची उटी कुमकुम केशरा
    [01:10] Chandanaachi Uti Kumkumkeshara
    [01:15] Smearing You with sandalwood paste and red kumkum on the forehead.
    
    [01:20] हिरेजडित मुकुट शोभतो बरा
    [01:20] Hirejadit Mukut Shobhato Bara
    [01:25] The diamond-studded crown suits You perfectly.
    
    [01:30] रुणझुणती नूपुरे चरणी घागरीया
    [01:30] Runjhunati Nupure Charani Ghagriya
    [01:35] Whose anklets tinkle melodiously on His feet.
    
    [01:40] लंबोदर पीतांबर फणिवर वंदना
    [01:40] Lambodar Pitaambar Phanivarvandana
    [01:45] The large-bellied Lord, wearing yellow silk, adorned with the serpent.
    
    [01:50] सरळ सोंड वक्रतुंड त्रिनयना
    [01:50] Saral Sond Vakratunda Trinayana
    [01:55] Who has a straight trunk, a curved snout, and three eyes.
    
    [02:00] दास रामाचा वाट पाहे सदना
    [02:00] Das Ramacha Vat Pahe Sadana
    [02:05] Ramdas (the devotee) waits for You in his home.
    
    [02:10] संकटी पावावे निर्वाणी रक्षावे सुरवरवंदना
    [02:10] Sankati Pavave Nirvani Rakshave Survarvandana
    [02:15] Please protect us during times of crisis, O Lord worshipped by the Gods.
    """,

    "epic hanuman chalisa": """
    [00:00] श्रीगुरु चरन सरोज रज, निज मनु मुकुरु सुधारि
    [00:00] Shri Guru Charan Saroj Raj, Nij Manu Mukuru Sudhaari
    [00:05] Cleansing the mirror of my mind with the dust from the Lotus-feet of Divine Guru.
    
    [00:10] बरनऊं रघुबर बिमल जसु, जो दायकु फल चारि
    [00:10] Baranau Raghubar Bimal Jasu, Jo Daayaku Phal Chaari
    [00:15] I describe the unblemished glory of Lord Rama, which bestows four fruits (Wealth, Righteousness, Desire, and Liberation).
    
    [00:20] बुद्धिहीन तनु जानिके, सुमिरौं पवन-कुमार
    [00:20] Buddhiheen Tanu Jaanike, Sumirau Pavan-Kumar
    [00:25] Knowing my body and mind to be devoid of intelligence, I remember the Son of the Wind.
    
    [00:30] बल बुधि बिद्या देहु मोहिं, हरहु कलेस बिकार
    [00:30] Bal Budhi Vidya Dehu Mohi, Harahu Kalesa Bikaar
    [00:35] Bestow upon me strength, wisdom, and knowledge, and remove all my miseries and blemishes.
    
    [00:40] जय हनुमान ज्ञान गुन सागर
    [00:40] Jai Hanuman Jyaan Guna Saagar
    [00:45] Victory to Hanuman, the ocean of wisdom and virtue.
    
    [00:50] जय कपीस तिहुं लोक उजागर
    [00:50] Jai Kapis Tihun Lok Ujaagar
    [00:55] Victory to the Lord of the Monkeys, who illuminates the three worlds.
    
    [01:00] राम दूत अतुलित बल धामा
    [01:00] Raam Doot Atulit Bal Dhaama
    [01:05] You are the messenger of Rama, the abode of immeasurable strength.
    
    [01:10] अंजनि-पुत्र पवनसुत नामा
    [01:10] Anjani-Putra Pavan Sut Naama
    [01:15] Known as the son of Anjani and the son of the Wind God.
    
    [01:20] महाबीर बिक्रम बजरंगी
    [01:20] Mahabeer Bikram Bajrangi
    [01:25] You are a great hero, exceptionally brave, with a body as strong as a thunderbolt.
    
    [01:30] कुमति निवार सुमति के संगी
    [01:30] Kumati Nivaar Sumati Ke Sangi
    [01:35] You dispel bad intellect and are the companion of good wisdom.
    
    [01:40] कंचन बरन बिराज सुबेसा
    [01:40] Kanchan Baran Biraaj Subesa
    [01:45] Your complexion is golden, and You are beautifully attired.
    
    [01:50] कानन कुंडल कुंचित केसा
    [01:50] Kaanan Kundal Kunchit Kesa
    [01:55] Wearing rings in Your ears and having curly hair.
    
    [02:00] हाथ बज्र औ ध्वजा बिराजै
    [02:00] Haath Bajra Au Dhvaja Biraajai
    [02:05] You hold a thunderbolt and a flag in Your hands.
    
    [02:10] कांधे मूंज जनेऊ साजै
    [02:10] Kaandhe Moonj Janeu Saajai
    [02:15] The sacred thread made of Munja grass adorns Your shoulder.
    
    [02:20] संकर सुवन केसरीनंदन
    [02:20] Sankar Suvan Kesari Nandan
    [02:25] You are the incarnation of Lord Shiva and the son of Kesari.
    
    [02:30] तेज प्रताप महा जग बन्दन
    [02:30] Tej Prataap Maha Jag Bandan
    [02:35] Your glory is vast, and You are revered by the whole world.
    
    [02:40] विद्यावान गुनी अति चातुर
    [02:40] Vidyavaan Guni Ati Chaatur
    [02:45] You are highly learned, virtuous, and exceptionally clever.
    
    [02:50] राम काज करिबे को आतुर
    [02:50] Raam Kaaj Karibe Ko Aatur
    [02:55] You are always eager to accomplish the tasks of Lord Rama.
    """,

    # ==========================================
    # WESTERN / ROCK / POP (Original English)
    # ==========================================

    "hotel california": """
    [00:53] On a dark desert highway, cool wind in my hair
    [00:59] Warm smell of colitas, rising up through the air
    [01:06] Up ahead in the distance, I saw a shimmering light
    [01:12] My head grew heavy and my sight grew dim
    [01:15] I had to stop for the night
    [01:19] There she stood in the doorway
    [01:22] I heard the mission bell
    [01:25] And I was thinking to myself
    [01:28] 'This could be Heaven or this could be Hell'
    [01:32] Then she lit up a candle and she showed me the way
    [01:39] There were voices down the corridor
    [01:42] I thought I heard them say
    [01:46] Welcome to the Hotel California
    [01:51] Such a lovely place (Such a lovely place)
    [01:54] Such a lovely face
    [01:59] Plenty of room at the Hotel California
    [02:04] Any time of year (Any time of year)
    [02:08] You can find it here
    [02:13] Her mind is Tiffany-twisted, she got the Mercedes Benz
    [02:19] She got a lot of pretty, pretty boys she calls friends
    [02:26] How they dance in the courtyard, sweet summer sweat
    [02:33] Some dance to remember, some dance to forget
    [02:39] So I called up the Captain
    [02:42] 'Please bring me my wine'
    [02:45] He said, 'We haven't had that spirit here since nineteen sixty-nine'
    [02:52] And still those voices are calling from far away
    [02:59] Wake you up in the middle of the night
    [03:02] Just to hear them say
    [03:05] Welcome to the Hotel California
    [03:11] Such a lovely place (Such a lovely place)
    [03:14] Such a lovely face
    [03:18] They livin' it up at the Hotel California
    [03:24] What a nice surprise (What a nice surprise)
    [03:27] Bring your alibis
    [03:33] Mirrors on the ceiling, the pink champagne on ice
    [03:39] And she said 'We are all just prisoners here, of our own device'
    [03:46] And in the master's chambers, they gathered for the feast
    [03:52] They stab it with their steely knives, but they just can't kill the beast
    [03:59] Last thing I remember, I was running for the door
    [04:05] I had to find the passage back to the place I was before
    [04:12] 'Relax,' said the night man
    [04:15] 'We are programmed to receive
    [04:19] You can check out any time you like
    [04:22] But you can never leave!'
    """,

    "bohemian rhapsody": """
    [00:00] Is this the real life?
    [00:03] Is this just fantasy?
    [00:06] Caught in a landslide
    [00:09] No escape from reality
    [00:14] Open your eyes
    [00:17] Look up to the skies and see
    [00:23] I'm just a poor boy, I need no sympathy
    [00:29] Because I'm easy come, easy go
    [00:33] Little high, little low
    [00:37] Any way the wind blows doesn't really matter to me, to me
    [00:49] Mama, just killed a man
    [00:54] Put a gun against his head
    [00:57] Pulled my trigger, now he's dead
    [01:00] Mama, life had just begun
    [01:07] But now I've gone and thrown it all away
    [01:14] Mama, ooh
    [01:21] Didn't mean to make you cry
    [01:25] If I'm not back again this time tomorrow
    [01:29] Carry on, carry on as if nothing really matters
    [01:41] Too late, my time has come
    [01:47] Sends shivers down my spine
    [01:50] Body's aching all the time
    [01:54] Goodbye, everybody, I've got to go
    [02:00] Gotta leave you all behind and face the truth
    [02:07] Mama, ooh (Any way the wind blows)
    [02:14] I don't wanna die
    [02:17] I sometimes wish I'd never been born at all
    [03:06] I see a little silhouetto of a man
    [03:09] Scaramouche, Scaramouche, will you do the Fandango?
    [03:13] Thunderbolt and lightning, very, very fright'ning me
    [03:17] (Galileo) Galileo, (Galileo) Galileo, Galileo Figaro magnifico
    [03:25] I'm just a poor boy, nobody loves me
    [03:28] He's just a poor boy from a poor family
    [03:32] Spare him his life from this monstrosity
    [03:38] Easy come, easy go, will you let me go?
    [03:41] Bismillah! No, we will not let you go
    [03:44] (Let him go!) Bismillah! We will not let you go
    [03:47] (Let him go!) Bismillah! We will not let you go
    [03:50] (Let me go) Will not let you go
    [03:52] (Let me go) Will not let you go
    [03:54] (Never, never, never, never let me go) Ah
    [03:57] No, no, no, no, no, no, no
    [04:00] (Oh, mamma mia, mamma mia) Mamma mia, let me go
    [04:04] Beelzebub has a devil put aside for me, for me, for me!
    [04:15] So you think you can stone me and spit in my eye?
    [04:21] So you think you can love me and leave me to die?
    [04:26] Oh, baby, can't do this to me, baby
    [04:32] Just gotta get out, just gotta get right outta here
    [04:54] Nothing really matters, anyone can see
    [05:04] Nothing really matters
    [05:09] Nothing really matters to me
    [05:21] Any way the wind blows
    """,

    "set fire to the rain": """
    [00:12] I let it fall, my heart
    [00:15] And as it fell, you rose to claim it
    [00:19] It was dark and I was over
    [00:22] Until you kissed my lips and you saved me
    [00:27] My hands, they were strong
    [00:30] But my knees were far too weak
    [00:34] To stand in your arms
    [00:37] Without falling to your feet
    [00:41] But there's a side to you that I never knew, never knew
    [00:45] All the things you'd say, they were never true, never true
    [00:49] And the games you'd play, you would always win, always win
    [00:53] But I set fire to the rain!
    [00:56] Watched it pour as I touched your face
    [01:00] Well, it burned while I cried
    [01:03] 'Cause I heard it screaming out your name, your name
    [01:10] When laying with you I could stay there
    [01:14] Close my eyes, feel you here forever
    [01:18] You and me together, nothing is better
    [01:25] 'Cause there's a side to you that I never knew, never knew
    [01:29] All the things you'd say, they were never true, never true
    [01:33] And the games you'd play, you would always win, always win
    [01:37] But I set fire to the rain!
    [01:41] Watched it pour as I touched your face
    [01:44] Well, it burned while I cried
    [01:47] 'Cause I heard it screaming out your name, your name
    [01:52] I set fire to the rain!
    [01:55] And I threw us into the flames
    [01:59] Well, it felt something died
    [02:02] 'Cause I knew that that was the last time, the last time
    [02:09] Sometimes I wake up by the door
    [02:13] That heart you caught must be waiting for you
    [02:16] Even now, when we're already over
    [02:20] I can't help myself from looking for you
    [02:24] I set fire to the rain!
    [02:28] Watched it pour as I touched your face
    [02:31] Well, it burned while I cried
    [02:34] 'Cause I heard it screaming out your name, your name
    [02:39] I set fire to the rain!
    [02:42] And I threw us into the flames
    [02:46] Well, it felt something died
    [02:49] 'Cause I knew that that was the last time, the last time
    [02:57] Oh, no
    [03:00] Let it burn
    [03:04] Oh, let it burn
    [03:08] Let it burn
    """,

    "aenema": """
    [00:42] Some say the end is near
    [00:46] Some say we'll see Armageddon soon
    [00:53] I certainly hope we will
    [00:57] I sure could use a vacation from this
    [01:03] Bullshit three-ring circus sideshow of freaks
    [01:11] Here in this hopeless fucking hole we call L.A.
    [01:18] The only way to fix it is to flush it all away
    [01:23] Any fucking time, any fucking day
    [01:28] Learn to swim, see you down in Arizona Bay
    [01:35] Fret for your figure and fret for your latte and
    [01:39] Fret for your lawsuit and fret for your hairpiece and
    [01:43] Fret for your Prozac and fret for your pilot and
    [01:47] Fret for your contract and fret for your car
    [01:51] It's a bullshit three-ring circus sideshow of freaks
    [01:59] Here in this hopeless fucking hole we call L.A.
    [02:05] The only way to fix it is to flush it all away
    [02:11] Any fucking time, any fucking day
    [02:16] Learn to swim, see you down in Arizona Bay
    [02:42] Some say a comet will fall from the sky
    [02:46] Followed by meteor showers and tidal waves
    [02:50] Followed by fault lines that cannot sit still
    [02:54] Followed by millions of dumbfounded dipshits
    [03:04] And some say the end is near
    [03:08] Some say we'll see Armageddon soon
    [03:13] I certainly hope we will
    [03:18] I sure could use a vacation from this
    [03:24] Stupid shit, silly shit, stupid shit
    [03:29] One great big festering neon distraction
    [03:36] I've a suggestion to keep you all occupied
    [03:41] Learn to swim
    [04:09] Mom's gonna fix it all soon
    [04:16] Mom's comin' 'round to put it back the way it ought to be
    [04:41] Learn to swim
    """,

    "vicarious": """
    [00:54] Eye on the TV, 'cause tragedy thrills me
    [00:58] Whatever flavor it happens to be like
    [01:02] Killed by the husband
    [01:04] Drowned by the ocean
    [01:06] Shot by his own son
    [01:08] She used a poison in his tea
    [01:12] And kissed him goodbye
    [01:14] That's my kind of story
    [01:17] It's no fun 'til someone dies
    [01:24] Don't look at me like I am a monster
    [01:28] Frown out your one face, but with the other
    [01:32] Stare like a junkie into the TV
    [01:36] Stare like a zombie while the mother holds her child
    [01:40] Watches him die
    [01:42] Hands to the sky crying, "Why, oh why?"
    [01:47] 'Cause I need to watch things die
    [01:51] From a distance
    [01:56] Vicariously I, live while the whole world dies
    [02:04] You all need it too, don't lie
    [02:20] Why can't we just admit it?
    [02:24] Why can't we just admit it?
    [02:28] We won't give pause until the blood is flowing
    [02:35] Neither the brave nor bold
    [02:37] Nor writers of stories told
    [02:39] We won't give pause until the blood is flowing
    [02:46] I need to watch things die
    [02:51] From a good safe distance
    [02:55] Vicariously I, live while the whole world dies
    [03:03] You all feel the same so why can't we just admit it?
    """
}

# --- 2. TESLA API HELPERS ---
def get_tesla_access_token():
    """Retrieves the Tesla API token securely from Streamlit secrets."""
    try:
        return st.secrets["TESLA_ACCESS_TOKEN"]
    except Exception:
        # Fallback for local testing before you add real secrets
        return "MOCK_TOKEN_FOR_TESTING"

def get_current_media_state(token, vehicle_id):
    """Polls the Tesla API for the currently playing track."""
    if token == "MOCK_TOKEN_FOR_TESTING":
        return {"title": "Hotel California", "artist": "Eagles", "is_playing": True}
        
    url = f"https://fleet-api.prd.api.tesla.com/api/1/vehicles/{vehicle_id}/vehicle_data"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            media_state = data.get("response", {}).get("vehicle_state", {}).get("media_state", {})
            return {
                "title": media_state.get("now_playing_title", ""),
                "artist": media_state.get("now_playing_artist", ""),
                "is_playing": media_state.get("media_playback_status") == "Playing"
            }
    except Exception as e:
        st.error(f"API Connection Error: {e}")
        
    return None

def find_lyrics(now_playing_title):
    """Robust fuzzy matching to find lyrics even if titles don't match exactly."""
    if not now_playing_title:
        return None
        
    search_title = now_playing_title.lower().strip()
    
    # 1. Try exact match first
    if search_title in LYRICS_DATABASE:
        return LYRICS_DATABASE[search_title]
        
    # 2. Try partial match (e.g. if Tesla says "Hotel California (Live)" but db says "hotel california")
    for db_title, lyrics in LYRICS_DATABASE.items():
        if db_title in search_title or search_title in db_title:
            return lyrics
            
    return None

# --- 3. STREAMLIT UI ---
st.title("🎵 Tesla Live Lyrics")

token = get_tesla_access_token()
# --- IMPROVED SECRET HANDLING ---
try:
    # This tries to get the real secret from Streamlit Cloud
    token = st.secrets["TESLA_ACCESS_TOKEN"]
    vehicle_id = st.secrets["TESLA_VEHICLE_ID"]
except Exception:
    # If the app is running locally, it uses these manual variables instead
    st.warning("Running in local mode. Please set your credentials.")
    token = "YOUR_MANUAL_TOKEN_HERE"
    vehicle_id = "YOUR_MANUAL_VEHICLE_ID_HERE"

# The dynamic auto-refresh block
with st.empty():
    while True:
        media = get_current_media_state(token, vehicle_id)
        
        if media and media["title"]:
            title = media["title"]
            artist = media["artist"]
            
            st.subheader(f"Now Playing: {title}")
            st.caption(f"Artist: {artist}")
            st.divider()
            
            # Lookup and display
            lyrics = find_lyrics(title)
            if lyrics:
                st.text(lyrics)
            else:
                st.info("🎵 Playing from USB drive. No custom lyrics found for this track in your database.")
                
        else:
            st.warning("Waiting for media data... Ensure the car is awake and music is playing.")
            
        # Refreshes the API every 5 seconds to stay within free tier limits
        time.sleep(5)
        st.rerun()
