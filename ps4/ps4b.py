# Problem Set 4B
# Name: Mogbeyi Emmanuel
# Collaborators:
# Time Spent: x:xx

import string
import pprint

### HELPER CODE ###
def load_words(file_name):
    """
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, "r")
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(" ")])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    """
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = "words.txt"


class Message(object):
    def __init__(self, text):
        """
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """

        self.text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        """
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        """
        return self.text

    def get_valid_words(self):
        """
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        """
        return self.valid_words

    def build_shift_dict(self, shift):
        """
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        """
        upper_case_letters = string.ascii_uppercase
        lower_case_letters = string.ascii_lowercase
        shifted_upper_case = self.form_shifted_letters(upper_case_letters, shift)
        shifted_lower_case = self.form_shifted_letters(lower_case_letters, shift)

        return self.convert_two_arrays_to_dic(
            upper_case_letters + lower_case_letters,
            shifted_upper_case + shifted_lower_case,
        )

    def form_shifted_letters(self, letters, shift):
        letters_array = [""] * len(letters)

        for i in range(len(letters)):
            letters_array[i] = letters[(i + shift) % 26]

        return letters_array

    def convert_two_arrays_to_dic(self, first_array, second_array):
        return {first_array[i]: second_array[i] for i in range(len(first_array))}

    def apply_shift(self, shift):
        """
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        """
        shifted_letters = self.build_shift_dict(shift)
        shifted_message_text = ""

        for char in self.text:
            if char in shifted_letters:
                shifted_message_text += shifted_letters[char]
            else:
                shifted_message_text += char

        return shifted_message_text


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        """
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)
        """
        Message.__init__(self, text)
        self.text = text
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        """
        Used to safely access self.shift outside of the class


        Returns: self.shift
        """
        return self.shift

    def get_encryption_dict(self):
        """
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        """
        return self.encryption_dict

    def get_message_text_encrypted(self):
        """
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        """
        return self.message_text_encrypted

    def change_shift(self, shift):
        """
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        """
        if shift < 0 or shift > 26:
            print("Shift must be greater than 0 and less than 26")
        else:
            self.shift = shift


class CiphertextMessage(Message):
    def __init__(self, text):
        """
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """
        self.text = text
        Message.__init__(self, text)

    def get_shift_freq(self):
        ''' 
        Gets the frequency of all shift key values.
        Returns a dictionary with the shift as the key
        and an array with the first element as the word count
        of each key and the sentence as the second element of the array
        '''
        shift_freq = {}

        for i in range(26):
            count = 0
            sentence = self.apply_shift(26 - i)
            words_of_sentence = sentence.split()

            for word in words_of_sentence:
                if is_word(self.valid_words, word):
                    count += 1
            shift_freq[i] = [count, sentence]

        return shift_freq

    def get_max_shift_value(self):
        '''
        Get maximum count value from frequency result
        '''
        values = self.get_shift_freq().values()
        return max([elem[0] for elem in values])

    def get_result(self, elem):
        '''
        Returns a tupple containing the shift with the maximum words and the 
        corresponding decrypted message
        '''
        result = ()
        shift_freq = self.get_shift_freq()

        for key, value in shift_freq.items():
            if value[0] == elem:
                result += (key, value[1])
        
        return result

    def decrypt_message(self):
        """
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        """

        max_value = self.get_max_shift_value()

        return self.get_result(max_value)


if __name__ == "__main__":

    #    #Example test case (PlaintextMessage)
    #    plaintext = PlaintextMessage('hello', 2)
    #    print('Expected Output: jgnnq')
    #    print('Actual Output:', plaintext.get_message_text_encrypted())
    #
    #    #Example test case (CiphertextMessage)
    #    ciphertext = CiphertextMessage('jgnnq')
    #    print('Expected Output:', (24, 'hello'))
    #    print('Actual Output:', ciphertext.decrypt_message())

    # TODO: WRITE YOUR TEST CASES HERE
    story = get_story_string()
    cipher = CiphertextMessage(story)
    decrypted_message = cipher.decrypt_message()
    print(decrypted_message)

    # TODO: best shift value and unencrypted story

    pass  # delete this line and replace with your code here
