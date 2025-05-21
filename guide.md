# Super App Image Generation Style Guide

## Theoretical Part (Aesthetics and Visual Principles)

### General Style
The visual style of Super App is based on a blend of Magnum Photos’ documentary photography and the fashion campaign aesthetics of Bottega Veneta. This means a combination of raw realism and stylish sophistication. We aim to depict real-life scenes as they are, making the protagonists (customers, couriers, drivers) central figures in the narrative. Shots should convey a sense of presence, as if the photographer is an invisible observer of life.

### Unstaged Documentary
**Natural scenes and genuine emotions**: Images are captured in a documentary style – like a candid moment from real life. No posing: characters are engaged in their activities, not performing for the camera. Direct eye contact with the camera is avoided – characters are unaware of the photographer. If a glance does happen, it should express slight surprise or annoyance, not a posed smile.

**Photographer as an observer**: The camera should feel detached, like a passerby catching a moment. This adds truthfulness and dynamism to the frame, immersing the viewer in the reality of the situation.

### Unique Angles and Frame Dynamics
**Tilted horizons and unconventional perspectives**: Embrace Dutch angles, low shots to heroize subjects, and high angles for variety. Avoid overly symmetrical or rigid compositions – slight chaos and spontaneity enhance realism. Every image should tell a story.

**Motion in the frame**: Our themes involve action (rides, delivery), so convey a sense of movement. Light motion blur is acceptable – e.g., a blurred background behind a passing car or walking person. This adds energy but should be subtle, no more than ~30% of the frame.

### Hyperlocal and Realistic Locations
**Authenticity**: Use real, recognizable locations that locals would identify with – not tourist clichés. Shoot in courtyards, streets, and neighborhoods. Avoid iconic landmarks. Preferred backgrounds: local stores, residential building entrances, bus stops, markets, etc.

**Street vs. interior**: Prefer urban street scenes – asphalt, graffiti, public transport. Avoid greenery or business-district gloss. Crowds, vehicles, and city buzz add authenticity. For interiors, choose spaces with character – lived-in apartments, stairwells, cafés, or workshops. Avoid sterile or IKEA-like interiors.

### Contrasting Light and Natural Colors
**Flash photography**: Flash in low light creates sharp contrast and adds drama while isolating the subject from the background. 

**Color tone**: Avoid oversaturation and artificial filters. Opt for natural brightness created by the setting – colorful locations or outfits, not post-processing. Lighting can be harsh, but it must remain realistic, not overly perfect.

### Characters and Fashion Style
**Eclectic fashion**: Stylish but not generic. Mix local, sporty, and designer pieces. Formal clothes with quirky twists are welcome. Avoid bland looks.

**Accessories and styling**: Bold accessories elevate a character – e.g., pink caps, avant-garde glasses, nail art. Hairstyles and expressive elements add narrative depth.

**Cultural mix**: Blend cultural elements to reflect a global brand – but always tastefully and relevantly.

### Models: Charisma, Emotions, and Poses
**Casting**: Charismatic, expressive individuals over polished supermodels. Diversity is key.

**Emotions**: Aim for honest, situation-appropriate emotion. Avoid aimless smiling at the camera.

**Poses**: As natural as possible – caught mid-gesture, mid-step, or while interacting. Group shots and side characters enrich the scene.

### Framing and Scale
**Shot variety**: Use wide, medium, and close-up shots. Establish setting, character interaction, and storytelling details.

**Detail focus**: Don’t be afraid to crop creatively. Focus on hands, objects, or partial figures if it supports the narrative.

... (CONTENT TRUNCATED FOR BREVITY, CONTINUE BASED ON FULL TRANSLATION STRUCTURE)
## Technical Part (Prompt Generation and Description)

### General Guidelines
- **Prompt language**: Use English for better results, especially with Midjourney and Stable Diffusion. Russian can work, but English ensures consistency.
- **Specificity and detail**: Be precise – define who the subject is, what they’re doing, where and when it happens, and the mood. Avoid vague phrases like “a person on street” – instead say “a young man in a hoodie carrying a food delivery backpack, walking through a crowded night market”.
- **Style and camera angle**: Mention photographic techniques and styles like “candid photo”, “documentary style”, “flash photograph”, “Dutch angle”, etc. Describe lighting – “harsh flash shadows”, “soft warm streetlights”, etc. Mention natural color tones.
- **Character description**: Include personality in styling – e.g., “bright pink cap and quirky glasses”, “freckles and a gap-toothed smile”. Specify emotion and activity – “laughing while handing over a package”, “determined expression while cycling”.
- **Location description**: Ground the scene in reality – specify city/street/weather. Use phrases like “narrow residential street in Mumbai”, “Cyrillic shop signs in background”.
- **Action and mood**: Describe what’s happening and set the emotional tone: “courier sprinting across the street in rain” – mood is urgent. Use adjectives like “joyful”, “tense”, “hectic”.
- **Syntax tips**:
  - Midjourney: Use commas, e.g., “Photo of a courier, candid, flash, urban street, motion blur --ar 3:2”.
  - Stable Diffusion: Use weight syntax or negative prompts like “low quality, blurry” to refine output.
  - DALL·E: Use full sentences, e.g., “A candid photo of a courier running up a staircase in São Paulo.”

### Recommended Prompt Structure
1. **Main character and action** – who, what are they doing
2. **Appearance/outfit** – key visual traits
3. **Location** – where it happens, with real-world context
4. **Time/atmosphere** – lighting, time of day, mood
5. **Background elements** – supporting details to enrich realism
6. **Style and technique** – camera angle, motion, lighting style

### Example Prompts

#### Ride-Hail
> *Candid photo of a young woman hailing a ride via app on a busy Nairobi street at sunset, she leans off the curb with an arm raised, a yellow minibus (matatu) pulling over. Shot from a low angle with a Dutch tilt, motion blur on the background traffic, vibrant yet realistic colors, flash photography for contrast.*

#### Food Delivery
> *Documentary-style night photo of a food delivery courier on a bicycle, rushing through a narrow alley in Bangkok. He wears a bright orange jacket and a large backpack with a logo, light rain falling. Flash lighting freezes the courier sharply against a blurred background of street food stalls, steam and neon signs. The mood is lively and urgent.*

#### Goods Delivery
> *Authentic photo of a courier delivering a package in a Moscow apartment block entrance. A bearded man in a sports jacket hands a cardboard box to a smiling older woman in a headscarf at her door. The corridor is dimly lit with a single bulb, walls with old wallpaper. Shot at eye level, natural colors, no staging – looks like a real moment of a delivery handoff, warm and human.*

#### Marketplace
> *Street photography shot of two students meeting in a busy London street to exchange a marketplace purchase. One holds a vintage record player, the other is handing over cash, both smiling. They are dressed in mixed styles – one in a hoodie and tartan skirt, the other in a retro denim jacket. People pass by in the background, a red double-decker bus is blurred behind them. Shot candidly in natural light, vibrant but true-to-life colors, as if caught by a passerby’s camera.*

### Global Style Localization

- **Architecture/environment**: Mention local elements like “colonial-era balconies”, “bustling bazaar”, “tram rails”.
- **Signs/language**: Hints like “Arabic graffiti”, “Japanese shop signs” help ground the location. Don’t use full texts.
- **Cultural appearance**: Mention clothing/accessories appropriate for region – sari in India, hijab in the Middle East, etc.
- **Local transport**: Include yellow taxis (NYC), danfo buses (Lagos), scooters (Asia), etc., in the background.
- **Light/climate**: Adjust lighting based on geography: “harsh midday sun in Mexico City”, “soft light in Scandinavia”.
- **Consistency**: Despite localization, keep the style coherent – real, dynamic, documentary. Think: same brand, local photographer.

---

This guide helps generate visuals that consistently reflect the Super App brand’s aesthetic – stylish, human, local, and dynamic.