# Telegram Bot Deployment Guide

## Railway Deployment Configuration

To avoid the "Conflict: terminated by other getUpdates request" error, configure your Railway deployment with these environment variables:

### Required Environment Variables:
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `OPENAI_API_KEY`: Your OpenAI API key

### Optional Environment Variables:
- `USE_WEBHOOK`: Set to "true" for production (recommended for Railway)
- `WEBHOOK_URL`: Your Railway app URL (e.g., https://your-app-name.railway.app)
- `PORT`: Port number (Railway sets this automatically)

### Recommended Railway Settings:
1. Set `USE_WEBHOOK=true` in your Railway environment variables
2. Set `WEBHOOK_URL` to your Railway app's public URL
3. Ensure only one instance is running at a time

### Troubleshooting:
- If you see conflict errors, check that only one bot instance is running
- Use webhook mode in production to avoid polling conflicts
- Monitor logs for any startup issues

---

# Style Guide for Super App Visual Prompts

## Overall Style  
[keywords: documentary, fashion, realism, unposed, energy]

### Aesthetic & Principles  
[keywords: street style, urban, flash, dynamic, real people]

- Style: Documentary realism × urban fashion  
- Subjects: Real people (customers, drivers, couriers)  
- Look: Unposed, genuine, mid-action  
- Angles: Low, high, Dutch tilt — dynamic framing  
- Lighting: Natural or flash, no filters or heavy editing  
- Color: Natural tones, vibrancy through detail  

---

## Characters  
[keywords: clothing, personality, accessories, realism]

Always specify the character’s nationality — for example, Colombian woman, Senegalese man, Zambian girl, Peruvian courier, Nigerian teenager etc.

Use precise present-tense verbs:

**The character should always perform only one action**
Good example: A girl walking parallel to the car
Bad example: A girl zipping her backpack, holding a phone

**Use precise present-tense verbs:** Stepping into, Biting into, Reaching for, Glancing toward, Holding, Fixing, Adjusting, Carrying, Offering, Zipping, Tapping, Squinting, Laughing, Waiting, Handing over

**Avoid:** *Posing, Standing still, Smiling at the camera, Portrait of*

**Examples (Do):**

- *A woman stepping out of a white Toyota Yaris*
- *A courier knocking on a gate with a delivery box under his arm...*
- *A young girl zipping her backpack*

**Examples (Don’t):**

- *A man holding a bag, looking around, fixing his jacket, walking toward the car.*
- *A woman eating, texting, waving, and opening the door.*
- *A teenager running, talking to someone, holding balloons, and smiling.*

Add an Emotional Layer

Even simple actions become expressive when they carry **inner emotion**. We avoid exaggerated grimaces or fake commercial smiles — we use **subtle, truthful expressions**, like in strong street or fashion photography.

### Emotions That Work:
**Calm / Cold**
*expressionless, jaw slightly tense, sharp eyes, neutral lips*
suits confident, fashion-forward looks

**Focused / Self-assured**
*calm focus, soft smirk, relaxed face, present but unreadable*
works for everyday or working scenes

**Lightness / Inspiration**
*gentle smile while looking down, subtle contentment, light posture*
fits quiet, inspiring moments

**Laughter — only between people**
*two people laughing naturally while doing something together*
allowed during interaction, but **not solo**

### Character Appearance  
[keywords: street fashion, layered, textured, accessories, visual hooks]

- Style: Street fashion — eclectic, layered, textured  
- Must-have: Accessories — nails, glasses, jewelry, standout elements  
- Avoid: Plain outfits, "office" looks, over-polished styling  


## Clothing
[keywords: Clothing, style, street fashion, layered, textured, accessories, visual hooks]

**Never Use Local or Traditional Clothing**
Clothing should be without Traditional prints — a mix of sporty and designer global brands.
Remove traditional patterns completely.

In Super App visuals, we avoid depicting characters in traditional or folkloric clothing — no matter how regionally authentic it may seem.

**Avoid:** 
*ceremonial African clothing, ethnic dress, folkloric attire, tribal outfits, native costume, heritage-style garments, festival wear, African cultural dress, ancestral robes, printed wax fabrics in full look, traditional textiles as full outfits, national dress, Afrocentric costumes, symbolic cultural wear, ornamental wraps and headscarves, village-style garments, pan-African prints head-to-toe, as well as similar traditional outfits from Latin America and Pakistan — such as Andean woven ponchos, folkloric embroidered blouses, mariachi-style pieces, Pakistani kurta-pajamas or sherwanis when styled as ethnic sets rather than streetwear-infused.*

Why?

- **We’re building a modern brand**: Our aesthetic reflects *today’s urban reality*, not historical or ceremonial imagery.
- **Local dress often looks outdated or stereotypical** when placed in contemporary, fashion-forward contexts.
- **Traditional elements can be used — but only as accents**: a pattern on a modern Accessories, a scarf styled with streetwear, etc. Never the full look.

### Women’s Looks — Street Fashion
[keywords: Woman style, woman, Woman Looks, wardrobe]


Convey personality through a **modern, eclectic look**.

Note: This is **street fashion**, not mass-market. Combinations should be bold. Accessories should be present, but not overdone.

**What works:**

Manicures can include nail art, not just solid colors — for women only.

- **Bold layering and contrasts**  
  Mix structured and soft pieces — denim with tulle, lace with sportswear, oversized with fitted.

- **Statement pieces**  
  Think heart-print pants, alien graphics, robe sets, or standout vintage jackets that define the look.

- **Accessories with personality**  
  Berets, mini bags, layered pearls, retro sunglasses, and beaded jewelry that add flair and individuality.

- **Unexpected pairings**  
  Football tees with lace skirts, track jackets with heels, graphic tops with midi skirts — surprising but stylish.

- **Shoes that anchor the look**  
  Chunky sneakers, combat boots, platform heels — always visible, always intentional.

- **Hair as part of the look**  
  Voluminous, styled, or wrapped — hair isn’t passive; it frames the face and adds attitude.

**DO (Examples)**

“woman in a cropped black jacket and electric blue high-waisted pants with bold white and striped detailing, white pointed heels”
→ Why: Bold silhouette and color pop — feels sharp, graphic, and cinematic

“woman wearing a red vest over a white tee, oversized light-wash jeans with a tie as a belt, round glasses, layered gold jewelry, and a patterned shoulder bag”
→ Why: Street meets vintage. Quirky details feel personal, lived-in

“girl in a bright blue graphic long-sleeve tucked into a cream midi skirt with front slit, mismatched colorful socks and chunky sneakers, bold accessories and a patterned shoulder bag”
→ Why: Energetic and playful. Contrasts and layering create depth

“woman sitting on a clear chair, wearing a lavender sweater with neon green alien heads, voluminous lime tulle pants, black beanie, and black-and-white sneakers”
→ Why: Fun, expressive, and memorable — fashion with a wink

“woman in a red Adidas track jacket paired with a short white lace skirt and red pointed heels, holding coffee and a large black handbag”
→ Why: Unexpected combo. High-low balance fits our eclectic vibe

“woman in a cropped black blazer with layered pearls, brooche, dramatic heart-print red trousers and oversized black sunglasses”
→ Why: Overstyled on purpose — feels bold, editorial, and smartly ironic

“woman wearing an oversized green football tee with yellow accents, flowing white lace-trimmed skirt and heavy black combat boots”
→ Why: Real-life eclecticism. Everyday pieces clashing beautifully

“woman in a white graphic tee, high-slit plaid skirt over matching maxi, platform boots, and a brown headscarf and trench thrown over the arm”
→ Why: Layered and textured — storytelling through outfit

“tall woman with voluminous hair in a bandeau top and oversized light denim palazzo pants, finished with a sheer balloon-sleeve robe”
→ Why: Cinematic proportions. Confident and airy, like a fashion moment

“girl in a blue graphic tee tucked into a layered tulle midi skirt, crossbody pouch bag, high-top sneakers, transparent tote with neon accessories, and a beret”
→ Why: Youthful and detail-rich — the kind of look you remember

“fashion-forward woman in a bold orange printed robe set, layered silver jewelry, retro sunglasses, neon sneakers, and a chartreuse mini bag”
→ Why: Strong color + personality — a full look, not a uniform

“Wearing a cropped mesh top under a loose jacket, layered beaded necklaces, yellow acrylic nails with cartoon decals”

“Braided hair with colorful clips and silver beads, scarf tied as a headband, glossy lips and bold hoop earrings”

---

### Men’s Looks — Street Fashion
[keywords: man style, man, man Looks, man wardrobe]
**Goal:** Express confidence and style through a **fashion blended street look**. Never overloaded — but there must be a statement. Accessories should be present, but minimal.

**What works:**

**Colorful manicures for men are not allowed**

- **Modern haircuts:** shaved sides, curls, color accents, neat braids
- **Headwear and scarves:** skullcaps, wraps, bucket hats, bandanas
- **Clothing:** a mix of athletic, designer, and casual wear
- **Clothing:** open shirts, vintage tees, sporty pants with flair
- **Shoes:** sneakers, bulky trainers, sandals with socks

**Example:**



- *Wearing a patterned tunic over jogger pants, layered with a bomber, gold ring on one hand and beaded bracelet on the other*
- *Short fade haircut with dyed tips, wraparound shades, and a silk scarf tied around the neck*

### Emotion & Posing  
[keywords: natural emotion, movement, walking, glancing, no eye contact]

- Emotion: Honest, subtle — focused, calm, neutral, or quietly fierce  
- Pose: In motion — walking, lifting, glancing. Never staged  
- Eyes: Not at camera — look away, sideways, down  

---

## Locations  
[keywords: urban, context, street, interior, real places]

Showcase country and culture through vibrant, real city context.

Locations must be **urban**, **realistic**, with **texture and personality**.

**Avoid:** parks, trees, greenery, "rural aesthetics."

### Urban Streets (Exterior)

**What works:**
- narrow city alleys*, concrete courtyards, roadside kiosks, *bus terminals, market crossings
- vendors, traffic, signs, exposed wires, billboards, graffiti
- dusty pavement, puddles, crumbling facades, taped posters, neon signs

**Examples:**
- on a cracked sidewalk in downtown Accra, with honking minibuses and street food smoke
- under faded billboards in central Medellín, next to a red tuk-tuk and stacked crates
- walking through a concrete alley in Cairo, graffiti walls and tangled wires overhead
- near a corner shop in Kinshasa, yellow kiosk with hand-painted ads, puddles on the street

**Avoid:**
- trees, palms, grass
- green parks or rural scenery
- country roads or "nature scenes"

**Rules:**
Always show the street from the side — a side-view perspective of a single side of the street: building façades, shop entrances, textured walls, balconies, cables.

Do not show wide symmetrical views of the whole street or street stretching into depth.
Do not describe the time of day in a stylized or cinematic way — avoid phrases like:
“against the harsh midday sun”
“bathed in golden hour light”
“morning haze”, “sunset glow”

Lighting should feel realistic and incidental, like ambient daylight or shadow from nearby buildings.


**Good Examples:**
“A woman walking along a narrow sidewalk, passing faded pink walls and a blue metal gate. Shot from the side, the white car is parked close to the building.”

“A man opening the rear door of a Yaris parked tight against a graffiti-covered wall.”

“A girl stepping toward a tuk tuk, only one side of the street is visible: old apartment balconies, peeling paint, and a broken sign above a metal shop gate.”

**Bad Examples:**
“A man walking down the middle of the street, buildings on both sides, golden hour sun behind him.”
Too wide. Too cinematic.

“A woman stepping out of a car as harsh sunlight flares across the road.”
Avoid stylized sunlight. Keep light natural and unremarkable.

### Background Activity 

The street should never feel empty. There should always be other people present — pedestrians, vendors, cyclists, seated figures — naturally integrated into the environment.

These background characters should appear:
in the background, walking, selling, talking, riding
or in the foreground, out of focus (blurred), cropped, partially visible

They should always be busy with their own tasks — not looking at the camera, not posing, and not interacting directly with the main character.

Use everyday street elements to support realism: benches, bicycles, crates, plants, laundry, handcarts, roadside chairs.

**Good Examples:**
“A woman walking toward a parked Yaris, while a cyclist passes by in the background. Farther behind, a vendor arranges mangoes on a wooden cart.”

“A man getting out of a car as a blurred figure crosses the frame in the foreground, holding plastic bags. Behind him, people sit on a bench under a shop awning.”

“A girl stepping into a tuk tuk. On the sidewalk behind her: an older man reads a newspaper near a cluster of potted plants. A boy walks a bicycle past the camera, slightly out of focus.”

**Bad Examples:**
“A man standing on an empty street, no one else around.”
Feels artificial and staged.

“A woman walking alone on a clean, symmetrical sidewalk.”
Too sterile. Missing texture and life.

### Interiors
Interiors should feel lived-in and cozy — not sterile or showroom-like. The spaces are personal, contemporary, and filled with small, meaningful details that reflect real life: textiles, everyday objects, open shelves, cups, plants, or gadgets. Rooms should feel warm, inhabited, and authentic — without being retro, broken down, or overly styled. Think soft light, visible signs of use, and elements that tell a story. The environment supports the character’s lifestyle and mood, blending effortlessly into the scene rather than standing out as decoration

What to avoid:
Interiors that look like showrooms or hotel rooms
Retro, run-down, or dirty spaces
Sterile or overly generic descriptions

**Do (Examples):**
“Inside a sun-filled kitchen with pale wooden cabinets, open shelves with colorful spice jars, and a kettle whistling on the stove. A cotton towel is draped over the oven handle, and the window curtain dances in the breeze.”

“A tidy living room with soft lighting, framed travel photos on the wall, and a woven basket filled with throw blankets next to a low couch. On the coffee table — a half-full tea mug and a book flipped open.”

“In a compact bathroom with light blue tiles, a toothbrush cup with two mismatched brushes, hand cream on the sink edge, and a mirror slightly fogged from a recent shower.”

**Don’t (Examples):**

“A clean modern kitchen with sleek furniture.”
Too cold and soulless

“A messy old room with broken wallpaper and rusted sink.”
Outdated and off-brand

“A simple bedroom with bed and chair.”
Lacks detail, emotion, and personality

Key elements to include:

Textiles: blankets, curtains, towels, napkins — for warmth

Tableware & food: plates, fruit, mugs, teapots — to add life

Lighting: soft daylight or warm evening tones (not retro)

Objects: books, plants, gadgets, cosmetics, candles — to emphasize modernity and individuality

---

## Framing & Composition  
[keywords: camera angle, wide shot, close-up, Dutch tilt, chaos]

- Vary shots:  
  - *Wide*: show place/context  
  - *Medium*: action/interaction  
  - *Close-up*: nails, food, screen, texture  
- Style: Cropped, unbalanced, chaotic. No centered portraits  
- Angles:  
  - *Dutch tilt*: adds energy  
  - *Low angle*: empowers subject  
  - *High angle*: adds casual observation  

---

## Prompt Structure  
[keywords: prompt format, description order, storytelling]

1. Main Character + Action  
   *e.g., A courier handing over a box through a gate*
2. Clothing / Appearance  
   *e.g., In a bright red jacket and black pants, neon nails*
3. Location & Environment  
   *e.g., Narrow alley in Kinshasa, street vendors nearby*
4. Time & Light  
   *e.g., Midday sun casting strong shadows, dust in the air*
5. Background Elements  
   *e.g., Faded posters, tangled wires, passing bikes*
6. Photography Style / Angle  
   *e.g., Low-angle shot with flash, candid frame*

---


## Ride-Hail 
[keywords: car, tuk tuk, motorcycle, red vehicle, Yaris, Picanto]

- Use white compact cars common and respectful for the country (Yaris, Picanto)  
- Driver is seated 
- Tuk-tuks and motorcycles should always be red  
- Passengers always sit in the back seat of the car  

### Walking to the car
Rules:
– The passenger is walking to or from the rear door of a white car
- The passenger can be walking parallel to the car
- The driver is already behind the wheel
- The shot captures only one side of the street (side view): building façades, storefronts, gates, textured walls — not a full street overview

Composition is slightly angled, often from the side or low

Examples:
“A woman walking toward the rear door of a white Toyota Yaris, her hand reaching for the handle. Behind her: pastel-painted walls, closed shopfronts, and a hanging wire. The driver is behind the wheel.”
“A man walking away from the car, one foot on the sidewalk, framed by chipped walls and a metal gate. The white Yaris is parked along the curb. Side view with soft golden light.”
“Wide-angle candid photo of a red tuk tuk pulling over on a busy street in Cali, Colombia. A street vendor slices mango into plastic cups under a striped umbrella in the foreground. Mid-frame: a fashionable young man steps out of the tuk tuk mid-motion, wearing baggy navy cargos, a cropped graphic tee under a loose mesh vest, and silver chains that catch the sunlight. His hair is braided with neon beads, and a black fanny pack hangs across his chest. The driver, partly visible in the mirror, adjusts his cap. The camera is angled low with a Dutch tilt, adding tension. Background blur reveals tangled overhead wires, old murals, and a passing moto taxi. Scene feels hot, fast, alive — dust catching the sharp midday light.”
“Wide-angle candid photo of a red tuk tuk pulling into a crowded street corner in Cali. In the foreground: a local man selling mango slices. Mid-ground: a fashionable young man stepping out of the tuk tuk — flared trousers, utility vest, multiple silver necklaces. In the background: the driver, visible in the mirror, wearing a blue button-up. Camera is tilted slightly for dynamism. Motion and street chaos create visual layering”
“A top-angle candid photo of a young Pakistani woman stepping out of a white Toyota Corolla in Lahore. She wears a red velvet shalwar kameez and chunky designer boots, carrying a paper shopping bag. Her long earrings swing as she moves. The car is parked on a narrow street with old bricks, fruit vendors, and motorbikes blurred in motion. Shot from above, cinematic motion, flash used to highlight textures, chaotic but authentic urban vibe”
“A young woman wearing a colorful alpaca wool cardigan swiftly goes to the rear door of white Toyota Corolla 2022, her large, geometric earrings glinting in the glow he morning sun. The scene is set on a busy cobblestone street in central La Paz, Bolivia, surrounded by vibrant market stalls and colonial architecture. The mood is fresh and invigorating, as the Andean light casts long, cool shadows across the scene. The photograph is taken from a high angle, allowing a bird's eye view of the action and providing a panoramic encompass of the old city's charm and chaos.”
“Caught in a wide-shot, a woman wearing an oversized jean jacket decorated with colorful patches, a black dress, bold Doc Marten boots, and rounded mirrored sunglasses, approaches a white Picanto parked in front of a streaked graffiti wall in downtown Barranquilla. The driver leans on the car, his features half-hidden in the shadow of his cap. The scene throbs with life as bikes whiz past in the background, the sun casts long, dramatic shadows across the cobblestone streets, embellishing the city's stoic vibrancy.”
“A young Colombian woman is moving towards the rear end of a red tuk-tuk on a bustling city street. Her outfit mixes streetwear with bold accents — she wears a fitted racer-back tank top under a cropped technical windbreaker with reflective panels, paired with ruched mini shorts and tall ribbed socks. Her accessories include chain necklaces and sunglasses on the head into her curls. Neon yellow nails against her phone, her other hand clutching a metallic micro-backpack. A side view of the street reveals traces of urban life: concrete building with graffiti, a tangle of electric wires, and locals darting by. Using dynamic framing, the shot is captured at a low camera angle.”

### Getting out of the car / tuk tuk
Rules:
- The passenger is getting out from the rear seat
- The driver is behind the wheel, but no mirrors or interior reflections are shown
- The shot shows physical motion: one leg out, torso turning, hand on the door

Examples:
“A woman getting out of the back seat of a white Toyota Yaris, her heel touching the sidewalk. The driver is behind the wheel.”

“A man stepping out, holding a bag close to his body, door wide open. The light casts long shadows across the side of the car.”


### Sitting in the back seat of a car
[keywords: inside, in the car, back seat, inside car, in the car]
Rules:
- Shot is from inside the car, showing only the back seat
- The driver is not mentioned
- The background is visible through the car window, showing local architecture or streetscape
- **Always add the entire phrase: Seat belt fastened** 
- **Always use shot from the front passenger seat**

Describe the interior: seat textures, materials, light reflections

 **Examples:**
“Camera angle & lens: Wide-angle close-up shot from the front seat, slightly over-the-shoulder, with shallow depth of field.
Location: Inside the back seat of a Toyota Yaris, urban street life of Nairobi visible through the window — street vendors, tangled power lines, faded posters on concrete walls.
Character & outfit: A young Kenyan woman, fashion-forward, wears a bright orange mesh top over a bralette, layered necklaces, and oversized cargo pants. Her long braids fall over her shoulder, with bold earrings peeking through. Neon nails grip the edge of the seat.
Action: She’s fastening her seat belt mid-movement, glancing casually out the window, one hand adjusting her phone on her lap.
Light & atmosphere: Late afternoon sun casts diagonal rays across the seat and her face. Dust motes float in the warm air.
Texture & detail: Seat fabric texture, glints from jewelry, worn edges of the seatbelt. The Yaris interior feels compact but lively.
Background: Through the window — blurred movement of pedestrians, a passing motorcycle, and handwritten chalk signs on nearby walls.”

“Camera angle & lens: Medium wide shot from the front passenger seat, eye level, slightly tilted.
Location: Backseat of a white Toyota Yaris 2023 parked on a sloping street in Medellín. Outside the window — brick houses with balconies, graffiti murals, and a street dog lounging nearby.
Character & outfit: A Colombian teenager in a patchwork hoodie, ripped jeans, and vibrant beaded bracelets. His hair is dyed blond at the tips. Seat belt fastened. 
Action: Sitting cross-legged, he’s scribbling something into a beat-up sketchbook, occasionally glancing out the window.
Light & atmosphere: Overcast sky casting soft diffused light through the windows, making interior shadows gentle.
Texture & detail: Pencil marks on his fingers, torn denim texture, condensation on the car window.”

“Main Character + Action: A young woman sits in the backseat of a Toyota Yaris 2023 car. Seat belt fastened. 
Clothing / Appearance: Dressed in an oversized denim jacket with gold chain, chunky rings and dangling earrings, her brightly colored nails tap rhythmically on her smartphone screen.
Location & Environment: Set against the backdrop of bustling Bogotá streets, vibrant murals line the sidewalks, hinting at the city’s artistic soul.
Time & Light: The late afternoon sun filters through the window, casting intricate patterns of light and shadow inside the car.
Background Elements: Cars whiz by in a colorful blur, and among them, street vendors push their carts filled with tropical fruit and snacks.
Camera angle & lens: Wide-angle close-up shot from the front seat, slightly over-the-shoulder, with shallow depth of field”

“Main Character + Action: A young man seats and leans back on the back seat of a Toyota Yaris 2023 car in the heart of Lusaka. Seat belt fastened. 
Clothing / Appearance: He sports a rolled-up sleeve leather jacket over a graphic t-shirt, a beaded necklace peeks out from under it. His hands, adorned in rings, casually hold a phone with a vibrant cover. 
Location & Environment: Through the car window, multi-storied buildings and hanging wires form the backdrop hinting at the urban buzz of Zambia. 
Time & Light: Dusty sunlight seeps in from the window adding depth to the scene. Background Elements: Cars whiz past, a boy sells groundnuts in the near distance, and an old billboard forms the last layer of this urban scene. 
Camera angle & lens: The frame is angled from the front seat offering a side view of the man and the scenery behind.”


“A girl sitting in the back seat of a white Yaris, scrolling through her phone. Through the window: concrete balconies and faded posters. Light hits the stitched leather seat.”

“A young man leaning back on a grey fabric headrest, phone in one hand. The street outside glows in a blur of graffiti walls and electric cables.”

### Sitting in the back of a tuk tuk
Rules:
- The passenger is always seated in the rear bench of the tuk tuk
- The driver is present, simply described as “at the wheel” — no close detail
- Framing may be from the side, from inside, or through the opening

Examples:
“A woman sitting in the back of a red tuk tuk, one hand resting on her lap, the other holding her phone. The driver is at the wheel.”

“A man seated in the back, looking out sideways, legs slightly apart. Flash lights up the vinyl seat. The driver is in front.”
“Low-angle shot of a Colombian guy sitting sideways in a red tuk tuk, leaning back casually with one leg up. He wears green wide-leg cargo pants, a vintage football jersey, and rectangular sunglasses. His ears are pierced with mismatched hoops. Flash reflects off his sweat-beaded forehead, and his woven crossbody bag rests on his lap. Scene feels hot, real, stylishly gritty”

### Sitting on the back of a motorcycle
[keywords: motorcycle, go to motorcycle, motorcycle, on motorcycle]
Rules:
- Use clear phrasing: “A person sitting behind the driver on the back of a motorbike”
- The driver is always present but only mentioned, not described
- Passenger is slightly off-balance or holding something

Examples:
“A young Nepali man sits on a red Bajaj Pulsar motorcycle, captured in a close-up from a sharp, low diagonal angle just behind the handlebar, focusing on his upper body. He wears a matte red full-face helmet with a reflective visor, turned slightly over his shoulder, revealing part of his thoughtful expression. His outfit is a layered streetwear look with a loose cream-colored cotton kurta under a sleeveless tan utility vest — blending traditional cuts with modern function. The natural light hits the curves of the helmet and vest, creating a cinematic highlight.
In the blurred background, a second person walks away along a concrete wall with faded graffiti, adding narrative depth. The setting is a Kathmandu alley with fallen leaves on the ground and muted city textures. The camera tilt and shallow depth of field create a dynamic, editorial framing that feels both raw and intentional — reminiscent of campaign stills from Yango or Kinfolk, but grounded in South Asian street context.”

“A fashion-forward Nepali man sits sideways on a red Bajaj Pulsar motorcycle parked on a dusty Kathmandu street, with his right leg over the seat and his left foot touching the ground. His helmet rests on the seat behind him. He wears a relaxed yet expressive outfit blending earthy and jewel tones: a lightweight patterned shirt with tribal and embroidered motifs, a draped loose jacket with vintage-inspired detailing, and wide-leg high-waisted pants made of raw textured cotton. His accessories include chunky silver rings and a narrow beaded necklace. His footwear is eclectic — hand-stitched leather loafers with visible wear. The camera is positioned at a slightly low and close angle, highlighting the motorcycle's curves and his silhouette against a backdrop of textured stone architecture and potted plants. Natural daylight with soft, warm shadows adds a candid documentary feel, merging local character with an elevated editorial streetwear aesthetic.”

“Shot from a low trailing angle just behind the rear wheel, a red Bajaj Pulsar glides through a dusty Kathmandu lane. The couple’s legs dominate the foreground — the woman wears cropped wide-leg cargo pants in washed charcoal with utility pockets and raw hems, paired with strappy leather sandals and a silver ankle cuff. Her upper half, partially visible, features a fitted ribbed tank top layered under an oversized, lightweight open jacket with faded patch graphics and frayed edges — casual, but expressive.
The man wears relaxed trousers and a loose cotton overshirt, both in earthy tones. Both riders wear matte black helmets, with the woman’s wavy hair pulled into a loose, low ponytail that moves slightly in the wind.
Their upper bodies rise into view with the backdrop of tangled Kathmandu street wires and aged brick textures. The light is diffused and warm, bouncing off metal and fabric folds. The overall composition captures urban motion with street-editorial flair — energetic, tactile, and rooted in contemporary Nepali culture.”

“A stylish young Nepali woman walks confidently past a red Bajaj Pulsar motorcycle on a narrow Kathmandu street. The camera captures her from a low, wide-angle perspective, emphasizing her movement and layered outfit. She wears a naturally dyed cotton dress with oversized sleeves, a patchwork vest made from vintage fabrics, and loose earthy-toned trousers with handcrafted embroidery at the cuffs. Her hair is softly waved and partially braided with beads, and she wears handmade jewelry. Her nails are painted in a soft, neutral shade. She glances down at her red phone, absorbed in thought as she walks.
In the background, slightly out of focus, a Nepali man sits on the parked Bajaj Pulsar, wearing a matte black helmet and layered streetwear with local textile patterns. His posture is relaxed but observant. Overhead wires, weathered walls, and signage place the scene clearly in Kathmandu. The natural daylight is diffused and cinematic, highlighting rich textures and vibrant but muted tones. The mood is editorial yet grounded — real, stylish, and subtly expressive of local culture.”

“A young Nepali man sits on a red Bajaj Pulsar motorcycle, captured in a close-up from a sharp, low diagonal angle just behind the handlebar, focusing on his upper body. He wears a matte red full-face helmet with a reflective visor, turned slightly over his shoulder, revealing part of his thoughtful expression. His outfit is a layered streetwear look with a loose cream-colored cotton kurta under a sleeveless tan utility vest — blending traditional cuts with modern function. The natural light hits the curves of the helmet and vest, creating a cinematic highlight.
In the blurred background, a second person walks away along a concrete wall with faded graffiti, adding narrative depth. The setting is a Kathmandu alley with fallen leaves on the ground and muted city textures. The camera tilt and shallow depth of field create a dynamic, editorial framing that feels both raw and intentional — reminiscent of campaign stills from Yango or Kinfolk, but grounded in South Asian street context.”

### Holding a phone with the vehicle in the background
Rules:
- Focus is on the passenger’s hand and phone — nails, rings, sleeves
- The vehicle is visible in the background, slightly blurred or partially framed (door, wheel, driver silhouette)
- The hand must be doing something: tapping, holding, swiping

Examples:
“Close-up of a hand with neon nails holding a phone, ride-hailing app open. In the background: a red tuk tuk with the driver at the wheel.”

“A woman holding her phone in front of her chest. The side of a white Yaris is visible behind, driver faintly seen through the glass.”

### Couple
[keywords: Couple, man and woman, two passengers, Two women, Two men, Mother and child, Father and child, Friends, two girls]

*Inside the car*


**Examples:**
*Inside car*
“A stylish Ivorian couple sitting together in the back seat of a clean white sedan taxi. She’s wearing a neon green wrap top and silver hoop earrings, her hand casually on his knee; he wears a brown mohair sweater with layered chains and a cap. Through the side window, glimpses of Abidjan pass by — market stalls, motorbikes, and rooftops. Shot from the front seat with shallow depth of field and warm interior light.”

*Inside car*
“A Nigerian woman and her younger sister sit in the back seat of a new sedan, viewed from the driver’s POV. The older sister wears a structured blazer and satin head wrap, relaxed but upright. The younger one clutches a pink purse and wears a graphic sweatshirt. They’re both buckled in. City textures — signs, umbrellas, faded walls — flicker behind them through the glass.”

*Inside car*
“A Zambian man and his younger brother sit in the back seat of a white Toyota sedan, shot from the driver’s POV. The older one wears a black-and-red bomber and bucket hat, watching something out the window. The boy wears a bright graphic tee and rests a bag on his knees. Seatbelts are on. Outside: glimpses of markets and street vendors pass by.”





## Food Delivery  
[keywords: food, steam, eating, home, interaction]

- Focus on delicious food — sauce, steam, textures  
- Include eating, serving, setting, or close-up food details  
- Use dynamic food interaction scenes  

## Parcel Delivery  
[keywords: courier, box, red top, handoff, biking]

- Courier in red top + black bottom (optional red cap)  
- kraft box (unbranded)  
- Show: knocking, hand-off, biking, standing with parcel  
- Key frames: hand-over, box detail, street scene  
