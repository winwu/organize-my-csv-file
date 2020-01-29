import getopt
import re

def get_total_user_val(argv):
    tmp_user_count = 0
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["itotal_user_count="])
    except getopt.GetoptError:
        print ('combine_category_by_user.py -i <total_user_count>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('combine_category_by_user.py -i <total_user_count>')
            sys.exit()
        elif opt in ("-i", "--itotal_user_count"):
            tmp_user_count = arg
            
    print('total user is: {}'.format(tmp_user_count))
    return tmp_user_count


def is_validate_csv_filename(alphabet, fname):
    # search pattern like: 1-A-1.csv ~ 1-A-3.csv
    if re.match("(^[1-9]-[" + re.escape(alphabet) + "]-[1-3]).csv", fname):
        return True
    return False