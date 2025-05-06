import requests

# Test /generate/blog
blog_resp = requests.post(
    "http://127.0.0.1:8000/generate/blog",
    json={
        "keywords": ["AI", "automation", "AI is better than sliced bread in Berry", "Postcode 2086", "Australia"],
        "language": "en",
        "word_count": 300,
        "format": "md",
        "frontmatter": {
            "title": "string",
            "meta_title": "string",
            "description": "string" ,
            "date": "datetime",
            "image": "string",
            "categories": "list[string]",
            "featured": "bool",
            "draft": "bool"
        },
        "components": ["quote"],
        "custom_rules": {"plain_direct_language": "Use short sentences and active voice. Define any technical terms immediately in simple words so readers never feel lost.", "reader_first_tone": "Write as an expert friend—confident and helpful, never salesy. Address the reader’s likely questions up front and speak to their needs (e.g., a first-home buyer vs. an experienced investor).", "eeat_signals_through_voice": "Weave in first-hand insights (“In my ten years as a mortgage broker…”), cite reputable sources (ASIC, RBA), and include a brief author bio with credentials to establish expertise and trust - in this case the author is Nathan Smith, Finance Author, the rest you can make up.", "concrete_examples_analogies": "Illustrate complex ideas (like compound interest) with relatable stories or numbers. Case studies or mini-scenarios make abstract concepts tangible.", "scannable_formatting": "Break text into 2–4-sentence paragraphs, use descriptive subheadings, bullets, call-out boxes for key takeaways, and bold or italicize terms for emphasis.", "human_edited_ai_drafts": "If you use AI to draft sections, rigorously fact-check and adapt its tone to your voice. Always prioritize accuracy and relevance for your Australian audience.", "inclusive_and_accessible": "Use respectful, jargon-free language that welcomes diverse readers. Ensure readability around an 8th-grade level and avoid assumptions about background or resources."        },
        "image_style": "A minimalistic, flat vector illustration. The color palette is limited to primary = #14c1bd, background = #ffffff and outlines = #083c44. Clean lines, no gradients, no textures, no words, text or fonts. Simple and professional icon-style design, with evenly spaced elements and ample white space.",
        "image_type": "webp",
        "image_size": "1536x1024",
        "image_url_suffix": "/images/blogs/"
    }
)
print("Blog endpoint response:", blog_resp.status_code, blog_resp.json())
