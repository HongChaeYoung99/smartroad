import os

class CLabelManager:
    config_path = './config/'
    cls_file = 'ClassMapping.csv'
    num_labels = 200
    used_labels = 0
    cls_map = {}

    def __init__(self, config_path='./', cls_file='ClassMapping.csv', num_labels=200):
        self.config_path = config_path
        self.cls_file = cls_file
        self.num_labels = num_labels

    def get_used_label(self):
        return self.used_labels

    def get_clas_map(self):
        return self.cls_map

    # 클래스이름 가져와주기
    def get_clas_name(self, nIdx):
        if nIdx > -1 and nIdx < self.used_labels:
            return self.cls_map[str(nIdx)]

        return 'none'

    # 우선 200개만큼 reserved로 채워주기
    def init_class_map(self):
        self.cls_map.clear()

        for i in range(self.num_labels):
            self.cls_map[
                str(i)] = 'reserved'  # 해당 데이터가 몇개의 라벨들로 이루어져있던지 200개 생성후 디폴트 라벨네임을 reserved로 설정하고, 값이 있으면 City_인천 등의 값으로 바꾸는거다

    # 0부터 내용 채워주기
    def load_class_map(self):

        used_labels = 0
        self.init_class_map()

        strFile = self.config_path + '/' + self.cls_file

        if os.path.isfile(strFile) == False:
            return '{} Not Exist'.format(self.cls_file)

        with open(strFile, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                elem = line.split(',')
                cls_name = elem[0].strip(' ')
                cls_label = elem[1].strip('\n')
                self.cls_map[cls_label] = cls_name

                self.used_labels = self.used_labels + 1
        return ''

    # 로그로 띄어줌
    def disp_cls(self):
        log = []
        for key, value in self.cls_map.items():
            log.append('label : {} class : {}'.format(key, value))
        return log

    # 세서 class_count.csv로 생성
    def write_cls_count(self, cls_tag, list_obj, cnt_train, cnt_test):
        # log = []

        print('used label = {}'.format(self.used_labels))

        #        output_csv_file = cls_tag + '.csv'
        output_csv_file = 'class_count.csv'

        with open(output_csv_file, 'a+') as fp:

            #            str_value = ('src data count \n')
            #            fp.write(str_value)

            str_value = ('{} train img ={}, test img = {}\n').format(cls_tag, cnt_train, cnt_test)
            fp.write(str_value)

            str_value = ('{}, {}, {} \n').format('label', 'class', 'count')
            fp.write(str_value)

            for key, value in self.cls_map.items():
                nKey = int(key)

                if nKey > -1 and nKey < self.used_labels:
                    #                   print('label = {}, class = {}, cnt = {}'.format(key, value, list_train_obj[nKey]))
                    str_value = ('{}, {}, {} \n').format(key, value, list_obj[nKey])
                    fp.write(str_value)