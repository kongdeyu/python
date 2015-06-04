#coding:utf-8


import math
import re


class WordsExtract(object):

    def __init__(self):
        self.longest_word_length = 5
        self.cohesiveness_threshold = 50
        self.entropy_threshold = 3
        self.dic_words = {}

    def from_file(self, file_name):
        content = ''
        f = file(file_name, 'r')
        for line in f:
            content += line.strip()
        self.from_string(content)

    def from_string(self, content):
        lst = self.__filter_invalid_characters(content)
        self.__words_frequence(lst)
        words_number = 0
        for word, info in self.dic_words.items():
            if info[0] > self.cohesiveness_threshold and info[1] > self.entropy_threshold:
                words_number += 1
                print word
        print words_number

    # private method
    def __filter_invalid_characters(self, content):
        # get Chinese characters, include punctuation
        pattern = re.compile(r'[\x80-\xff]{3}')
        lst = pattern.findall(content)

        # filter punctuation
        pattern = re.compile(r'　|。|；|，|：|“|”|（|）|、|？|《|》|\s|【|】|《|》|／|！|─|…')
        lst = [item for item in lst if not pattern.match(item)]
        return lst

    def __words_frequence(self, lst):
        words_number = 0
        words_frequence = {}
        words_left_neighbor = {}
        words_right_neighbor = {}
        word_length = 0

        # calculate word frequence
        while word_length < self.longest_word_length:
            word_length += 1

            # calculate statistics for words whose length is word_length
            for index in range(len(lst) - word_length + 1):
                current_word = ''.join(lst[index: index + word_length])
                if current_word not in words_frequence:
                    words_number += 1

                    # initialize frequence
                    words_frequence[current_word] = 1
                    # initialize neighbor
                    left_neighbor = {}
                    left_neighbor[index - 1 >= 0 and lst[index - 1] or ''] = 1
                    words_left_neighbor[current_word] = left_neighbor
                    right_neighbor = {}
                    right_neighbor[index + word_length < len(lst)
                            and lst[index + word_length] or ''] = 1
                    words_right_neighbor[current_word] = right_neighbor
                else:
                    # update frequence
                    words_frequence[current_word] += 1
                    # update neighbor
                    left_neighbor = (index - 1 >= 0 and lst[index - 1] or '')
                    if left_neighbor not in words_left_neighbor[current_word]:
                        words_left_neighbor[current_word][left_neighbor] = 1
                    else:
                        words_left_neighbor[current_word][left_neighbor] += 1

                    right_neighbor = (index + word_length < len(lst)
                            and lst[index + word_length] or '')
                    if right_neighbor not in words_right_neighbor[current_word]:
                        words_right_neighbor[current_word][right_neighbor] = 1
                    else:
                        words_right_neighbor[current_word][right_neighbor] += 1

        print words_number
        self.__words_density(words_frequence, words_number)
        self.__words_entropy(words_left_neighbor, words_right_neighbor)

    def __words_density(self, words_frequence, words_number):
        for word, frequence in words_frequence.items():
            info = []
            if len(word) == 3:
                info.append(1)
            else:
                f1 = words_frequence[''.join(word[0: 3])] * words_frequence[''.join(word[3:])]
                f2 = words_frequence[''.join(word[0: -3])] * words_frequence[''.join(word[-3:])]
                info.append(frequence * words_number / (f1 > f2 and f1 or f2))
            self.dic_words[word] = info

    def __words_entropy(self, words_left_neighbor, words_right_neighbor):
        for word, neighbor_info in words_left_neighbor.items():
            neighbor_sum = 1
            temp = 1
            for neighbor, number in neighbor_info.items():
                neighbor_sum += number
                # get Σ(Xi*lgXi)
                temp += number * math.log(number)
            entropy = math.log(neighbor_sum) - temp / neighbor_sum;
            self.dic_words[word].append(entropy)

        for word, neighbor_info in words_right_neighbor.items():
            neighbor_sum = 1
            temp = 1
            for neighbor, number in neighbor_info.items():
                neighbor_sum += number
                # get Σ(Xi*lgXi)
                temp += number * math.log(number)
            entropy = math.log(neighbor_sum) - temp / neighbor_sum;
            if self.dic_words[word][1] > entropy:
                self.dic_words[word][1] = entropy


def error(Exception):
    pass
