from EnglishModel import EnglishModel

def main():
    model = EnglishModel(['bible-kjv.txt'])

    print "(King James) Sample Text:"
    print model.produce(45)
    print

    print "HE commands:"
    for i in range(10):
        print model.produce(20, "thou shalt")
    print

    print "what does HE do:"
    for i in range(10):
        print model.produce(20, "LORD hath")

if __name__ == '__main__':
    main()
