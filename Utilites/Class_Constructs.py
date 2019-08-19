import sys


class AlfaDog(object):

    '''I parse Alfa output files'''

    version = '1.0'

    def __init__(self, file_path, d_y, d_m, d_d):
        self.file_path = file_path
        self.d_y = d_y
        self.d_m = d_m
        self.d_d = d_d

    def __str__(self):
        return self.file_path + '\n' + str(self.d_y) + '\n' + str(self.d_m) + '\n' + str(self.d_d)

    ''' Custom constructor for date from string '''
    @classmethod
    def date_from_str(cls, file_path, date_str):
        ''' pass date_str arg as 'yyyy-mm-dd' or 'yyyy/mm/dd' '''
        try:
            y,m,d = map(int, date_str.split('-'))
        except:
            print('no dash')
        try:
            y,m,d = map(int, date_str.split('//'))
        except:
            print('no slash')
        return cls(file_path, y, m, d)

    def __iter__(self):
        self.iterator = 0
        self.tokens = self.file_path.split('\\')
        self.n = len(self.tokens)
        return self

    def __next__(self):
        if self.iterator < self.n:
            result = self.tokens[self.iterator]
            self.iterator += 1
            return result
        else:
            raise StopIteration

    def get_file_ext(self):
        filename, file_extension =  path.splitext(self.file_path)
        return file_extension


if __name__ == '__main__':

    c = AlfaDog(sys.argv[1], 2019, 10, 2)
    d = AlfaDog.date_from_str(sys.argv[1], '2019-10-02')
    e = AlfaDog.date_from_str(sys.argv[1], '2019//10//02')

    print('******** c *********')
    print(c.d_d, c.d_m, c.d_y)
    print('******** d *********')
    print(d.d_d, d.d_m, d.d_y)
    print('******** e *********')
    print(e.d_d, e.d_m, e.d_y)
