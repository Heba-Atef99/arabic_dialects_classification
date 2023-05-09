import re
import string
import emoji

arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
english_punctuations = string.punctuation
punctuations_list = arabic_punctuations + english_punctuations
arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)

def remove_tags(text):
  return re.sub(r'@\w*\s', '', text)

def remove_numbers(text):
  return re.sub(r'\d', ' ', text)

def remove_links(text):
    # the re.DOTALL flag is used to match across multiple lines,
    # in case the link spans multiple lines in the input text.
    link_pattern = re.compile(r'https?://\S+|www\.\S+', re.DOTALL)
    return link_pattern.sub(' ', text)

def remove_english_characters(text):
    english_characters_pattern = re.compile(r'[a-zA-Z]+')
    return english_characters_pattern.sub(' ', text)

def remove_punctuation(text):
    return text.translate(str.maketrans(punctuations_list, ' '*len(punctuations_list)))

def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text

def remove_repeating_char(text):
    return re.sub(r'(.+)\1{2,}', r'\1', text)

def remove_tabs_and_new_lines(text):
    return re.sub(r'[\n\t]+', ' ', text)

def normalize_arabic(text):
    text = re.sub("[ٱإأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text

def get_emoji_regexp():
    # Sort emoji by length to make sure multi-character emojis are
    # matched first
    emojis = sorted(emoji.EMOJI_DATA, key=len, reverse=True)
    pattern = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'
    return re.compile(pattern)

emoji_pattern = get_emoji_regexp()

def remove_emojis(text):
    return emoji_pattern.sub(' ', text)

def preprocess_text(text):
    text = remove_tags(text)
    text = remove_numbers(text)
    text = remove_links(text)
    text = remove_english_characters(text)
    text = remove_punctuation(text)
    text = remove_diacritics(text)
    text = remove_repeating_char(text)
    text = remove_tabs_and_new_lines(text)
    text = normalize_arabic(text)
    text = remove_emojis(text)
    return text