from collections import Counter
import nltk
import ssl
import re

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from nltk.corpus import words, names

nltk.download('words', quiet=True)
nltk.download('names', quiet=True)
word_list = words.words()
name_list = names.words()

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def encrypt(txt, cipher_key):
  encrypted_text = ""

  for char in txt:
    if char == " ":
      encrypted_text += " "
      continue
    string_test = char.isalpha()
    if not string_test:
      encrypted_text += char
      continue
    cleaned_input = char.lower()
    alpha_index = alphabet.index(cleaned_input)
    shift_num = (alpha_index + cipher_key) % 26
    shifted_char = (alphabet[shift_num])
    if char.isupper():
      encrypted_text += shifted_char.upper()
    else:
      encrypted_text += shifted_char

  return encrypted_text


def decrypt(encrypted_txt, cipher_key):
  return encrypt(encrypted_txt, -cipher_key)

def crack(encrypted_txt):
  counted = Counter(encrypted_txt)
  common = counted.most_common(2)
  common_letter = ""

  for char in common:
    if not char[0] == " ":
      common_letter = char[0]

  e_index = alphabet.index("e")
  t_index = alphabet.index("t")
  encrypt_index = alphabet.index(common_letter)
  e_num = 0
  t_num = 0


  for num in range(0,26):
    shift_num_t = (t_index + num) % 26
    if shift_num_t == encrypt_index:
      t_num = num
    shift_num_e = (e_index + num) % 26
    if shift_num_e == encrypt_index:
      e_num = num

  t_decrypt = decrypt(encrypted_txt, t_num)
  e_decrypt = decrypt(encrypted_txt, e_num)
  removed_t = re.sub("[^\w\s]","", t_decrypt)
  removed_e = re.sub("[^\w\s]","", e_decrypt)
  word_test_t = removed_t.split(' ')
  word_test_e = removed_e.split(' ')

  true_list_t = []
  for word in word_test_t:
    if word.lower() in word_list:
      true_list_t.append("true")
    else:
      print(word)

  true_list_e = []
  for word in word_test_e:
    if word.lower() in word_list:
      true_list_e.append("true")
    else:
      print(word)

  if len(true_list_t) == len(word_test_t):
    return t_decrypt
  elif len(true_list_e) == len(word_test_e):
    return e_decrypt
  else:
    return ""

