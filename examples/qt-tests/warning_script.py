from time import sleep
import warnings


def main():
    sleep(3)

    warnings.warn("This is a warning, but the process shouldn't fail")

    sleep(5)



if __name__ == '__main__':
    main()