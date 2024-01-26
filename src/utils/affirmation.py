import random


def calculate_time_difference_seconds(start_at, end_date):
    # Calculate the time difference in seconds
    time_difference_seconds = (end_date - start_at).total_seconds()

    return time_difference_seconds


def generate_random_sentence():
    subjects = [
        "I",
        "You",
        "He",
        "She",
        "It",
        "We",
        "They",
        "The professor",
        "My friend",
        "A mysterious stranger",
    ]
    verbs = [
        "run",
        "eat",
        "sleep",
        "write",
        "sing",
        "dance",
        "explore",
        "discover",
        "contemplate",
        "analyze",
    ]
    adverbs = ["quickly", "slowly", "happily", "curiously", "effortlessly", "intently"]
    adjectives = [
        "beautiful",
        "mysterious",
        "colorful",
        "enchanting",
        "captivating",
        "intriguing",
    ]
    objects = [
        "a book",
        "the cat",
        "a song",
        "an apple",
        "the beach",
        "a movie",
        "a magnificent painting",
        "a hidden treasure",
    ]

    sentence = f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(adverbs)} {random.choice(adjectives)} {random.choice(objects)}."
    return sentence


def generate_random_sentences(num_sentences):
    sentences = [generate_random_sentence() for _ in range(num_sentences)]
    return sentences
