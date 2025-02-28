from textract import ocr
def test_ocr(coef, text_ocr, text_str):
    text_str = set(text_str.split())
    text_list = set(text_ocr.split())
    common_items = text_list.intersection(text_str)
    
    # Calculate similarity as a percentage
    similarity = (len(common_items) / max(len(text_list), len(text_str))) * 100
    print(similarity)
    res = similarity >= coef
    if not res:
        print(text_ocr)
    
    
    return res

# white background 1 paragraph
assert(test_ocr(90,ocr("media/i6.jpg"), 
"English texts for beginners to practice reading and comprehension online and for free. Practicing your comprehension of written English will both improve your vocabulary and understanding of grammar and word order. The texts below are designed to help you develop while giving you an instant evaluation of your progress."))

# dark background 1 paragraph
assert(test_ocr(90, ocr("media/i8.jpg"), "Nature is a source of endless inspiration and wonder. From the majestic mountains to the serene oceans, it offers a diverse array of landscapes that captivate the human spirit. The chirping of birds, the rustling of leaves, and the gentle flow of rivers remind us of the harmony and balance that exist in the natural world."))

#dark background 3 paragraphs
assert(test_ocr(90, ocr("media/i7.jpg"), """The Wonders of Technology Technology plays a vital role in shaping the modern world. From smartphones to AI, it’s impossible to ignore its influence. Innovations like autonomous cars & wearable devices bring convenience and efficiency into our lives. Many industries, including healthcare, education, and entertainment, rely on tech to thrive. For example, apps & online platforms allow people to stay connected regardless of distance. Imagine this: a virtual meeting with participants from 5+ countries, all collaborating seamlessly—this is the magic of tech! But with progress comes responsibility. It’s up to us to ensure that advancements are used ethically & sustainably. After all, technology should improve lives—not complicate them."""))

assert(test_ocr(90,ocr("media/i9.jpg"), 
"English texts for beginners to practice reading and comprehension online and for free. Practicing your comprehension of written English will both improve your vocabulary and understanding of grammar and word order. The texts below are designed to help you develop while giving you an instant evaluation of your progress."))
