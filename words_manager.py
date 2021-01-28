import random

data_source_file = ['br-utf8.txt']

class WordSpitter():

    def __init__(self, filename):
        ''' constructor '''
        try:
            self.size, self.words = self.get_words(filename)
        except:
            print('Ops, something wrong opening the word dictionary')
            self.size = 1
            self.words = ['error'] 

        
    def get_words(self, file_name):
        ''' returns word count and words from file '''
        f = open(file_name, 'r', encoding='utf8')
        words = f.readlines()
        size = 0
        for _ in words:
            size += 1

        print('No de linhas = ', size)
        f.close()

        return size, words
    
    def sort_words(self, n):
        ''' sort "n" random words whithout duplicates'''
        
        # Generate list of random indexes
        idxs = [random.randint(0, self.size-1) for i in range(n)]
         
        # Check for duplicates:
        duplicates = [idxs.count(i) > 1 for i in idxs]
        contains_duplicates = any(duplicates)

        while contains_duplicates:
            # Remove duplicates:
            for i, idx in enumerate(idx):
                # Find where the duplicates are.
                if duplicates[i] == True:
                    # New index
                    idxs[i] = random.randint(0, self.size-1)
            
            # Check for duplicates:
            duplicates = [idxs.count(i) > 1 for i in idxs]
            contains_duplicates = any(duplicates)

        
        selected_words = [self.words[i].strip('\n') for i in idxs]

        return selected_words


if __name__ == '__main__':
    # Criar um obj
    wordSpitter = WordSpitter('br-utf8.txt')

    ws = wordSpitter.sort_words(10)

    for w in ws:
        print(w)