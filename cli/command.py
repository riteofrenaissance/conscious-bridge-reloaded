
# في بداية الملف أضف:
import cli.utils as utils

# في دالة status أضف:
utils.print_project_info()

# أوامر جديدة:
elif command == "info":
    utils.print_project_info()
elif command == "scripts":
    utils.list_scripts()
elif command == "quick":
    utils.quick_check()
