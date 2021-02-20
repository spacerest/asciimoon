settings = {
	"numbers-reversed": 
			{
			"ascii_dims": (10, 10),
			"settings_type": "linear",
			"symbols": {"young_moon": [str(x).zfill(2) for x in reversed(range(100))],
						"old_moon": [str(x).zfill(2) for x in reversed(range(100))]
					}
			},
	"numbers": 
			{
			"ascii_dims": (10, 10),
			"settings_type": "linear",
			"symbols": {"young_moon": [str(x).zfill(2) for x in range(100)],
						"old_moon": [str(x).zfill(2) for x in range(100)]
					}
			},

	"numbers-emojis": 
			{
			"ascii_dims": (10, 10),
			"settings_type": "linear",
			"symbols": {
				"young_moon": [" ⓪ "," ⓵ "," ② "," ⓷ "," ⓸ "," ⓹ "," ⑥ "," ⓻ "," ⓼ "," ⓽ "],
				"old_moon": [" ⓪ "," ⓵ "," ② "," ⓷ "," ⓸ "," ⓹ "," ⑥ "," ⓻ "," ⓼ "," ⓽ "]
			}
			},
	"moons":
			{
			"ascii_dims": (10, 10),
			"settings_type": "random",
			"symbols": {
				"young_moon": ["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌒","🌒","🌒","🌒","🌒","🌒","🌒","🌓","🌓","🌓","🌓","🌓","🌓","🌓","🌔","🌔","🌔","🌔","🌔","🌔","🌔","🌔","🌔","🌔","🌕"],
				"old_moon": ["🌑","🌘","🌗","🌔","🌕"],
				"random_shadow_symbols" : ["💥","💨","🦊","🐨","🦇","🦔","🦚","🦎","🐍","🐢","🐊","🐬","🐋","🦖","🦕","🐉","🐲","🐟","🐠","🦈","🐚","🦋","🕸","🌱","🌵","🍁","🍂","🦑","🔥","🌊","☄","⛈","🌿","☘","🍀","🦗","💎","✂️","♻️","💿","💾","📼","📷","🏔","🌨","🌎","🥀","🌷","🌸","🐾","🐌","🐏","🐻","💍","🧶"],
				"random_light_symbols" : ["💥","💨","💫","🦊","🐨","🦇","🦔","🐣","🦚","🦎","🐍","🐢","🐊","🐬","🐋","🦖","🦕","🐉","🐲","🐟","🐠","🦈","🐚","🦋","🕸","🌱","🌵","🍁","🍂","🦑","🌈","⚡","🔥","🌊","✨","☄","⛈","🌾","🌿","☘","🍀","🦗","📸","📀","🔑","🏔","🌨","🌎","🥀","🌷","🌸","🐾","🐌","🐏","🐻","💍","🧶"],
				}
			}

}