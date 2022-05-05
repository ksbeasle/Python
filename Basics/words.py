from urllib.request import urlopen


def words():
    story = urlopen('http://sixty-north.com/c/t/t.txt')  # RIP to this link
    story_words = []
    for line in story:
        line_words = line.decode('utf-8').split()
        for word in line_words:
            story_words.append(word)
    story.close()
    return
