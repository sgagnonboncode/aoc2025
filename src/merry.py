from colorama import Fore, Back, Style


# display the current solver with some fancy x-mas colors
def display_splash_title(puzzle_id: int = 1) -> None:
    banner = [
        Fore.YELLOW + "         |",
        Fore.YELLOW + "        -+-",
        Fore.YELLOW + "         A",
        Fore.GREEN + "        /=\\            ",
        Fore.GREEN
        + "      "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "/ "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + " \\"
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "          ",
        Fore.GREEN + "      /=====\\          ",
        Fore.GREEN
        + "      /  "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "  \\         "
        + Fore.RED
        + "      _    ___   ____   ____   ___ ____  ____",
        Fore.GREEN
        + "    "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "/ "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + " * "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + " \\"
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "       "
        + Fore.RED
        + "     / \\  / _ \\ / ___| |___ \\ / _ \\___ \\| ___|",
        Fore.GREEN
        + "    /=========\\       "
        + Fore.RED
        + "    / _ \\| | | | |       __) | | | |__) |___ \\",
        Fore.GREEN
        + "    /  *   *  \\       "
        + Fore.RED
        + "   / ___ \\ |_| | |___   / __/| |_| / __/ ___) |",
        Fore.GREEN
        + "  "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "/ "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + "   "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "   "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + " \\"
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "     "
        + Fore.RED
        + "  /_/   \\_\\___/ \\____| |_____|\\___/_____|____/",
        Fore.GREEN + "  /=============\\      ",
        Fore.GREEN
        + "  /  "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + "   "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "   "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + "  \\      "
        + Fore.WHITE
        + f"                   Day {puzzle_id:02d}"
        + Fore.GREEN,
        Fore.GREEN
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "/ *   "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + "   "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + "   * \\"
        + Fore.WHITE
        + "i"
        + Fore.GREEN,
        Fore.GREEN + "/=================\\",
        Fore.BLACK + "       |___|",
    ]

    for banner_line in banner:
        print(Fore.RED + banner_line + Fore.RESET)

    print(Style.RESET_ALL)
