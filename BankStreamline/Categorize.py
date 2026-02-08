

import polars as pl



def make_categories(df):

    df = df.with_columns(category = 
                    # ======================= Food =======================
        pl.when(pl.col('description').str.contains('McDon|CORPORATE|CHICK-FIL-A|SLIM CHICKENS')).then(pl.lit('food'))
        .when(pl.col('description').str.contains('MADDIES PLACE|RAISING CANES|Subway|HICKORY|HUDSONS')).then(pl.lit('food'))
        .when(pl.col('description').str.contains('JAMBA|PIZZA|GOODCENTS|SONIC|TACO BELL|BUFFET|NOVO COFFEE')).then(pl.lit('food'))
        .when(pl.col('description').str.contains('Waffle House|DAIRY QUEEN|COLDSTONE|MCGRAWS|HUDSONNEWS')).then(pl.lit('food'))
        .when(pl.col('description').str.contains('LITTLE CAESARS|MCDON|WENDY|APPLEBEES|PERCY|TASTES ON THE FLY')).then(pl.lit('food'))
        .when(pl.col('description').str.contains('EL SUR|BAREFOOT BISTRO|YAMATO|SMOOTHIE|CREAMERY')).then(pl.lit('food'))
        .when(pl.col('description').str.contains('DOLLAR GENERAL|DOLLAR TREE|FLYING BURGER|WWW.HOMECHEF.IL')).then(pl.lit('food'))
        .when(pl.col('description').str.contains('DOMINO.S|POPEYES|COCA COLA|LA VILLA MEXICAN|PJ\'S COFFEE')).then(pl.lit('food'))
        .when(pl.col('description').str.contains('CRCKR BRRL|OFF THE RAIL CAFE|HOUSE-WYLIE|SWOLE FOOD')).then(pl.lit('food'))
        .when(pl.col('description').str.contains('DC FUDDRUCKERS|THE BLACK CAT CAFE|RHEA LANA|BYUI FOOD')).then(pl.lit('food'))
        .when(pl.col('description').str.contains('WHATABURGER|CUPBOP|TASTY DONUTS|HELLA FRESH|JOHNNY B\'S GRILL')).then(pl.lit('food'))
        .when(pl.col('description').str.contains('WILDCAT SNACK|ARBYS|SNACKS ABUELITA|MURPHY 1111')).then(pl.lit('food'))
                    # ======================= subscriptions =======================
        .when(pl.col('description').str.contains('Adobe|Spotify|Phtoshp Lightrm|Peacock')).then(pl.lit('subscriptions'))
        .when(pl.col('description').str.contains('WMT PLUS|HEALTHWORKS|APPLE.COM/BILL|SAFE HAVEN')).then(pl.lit('subscriptions'))
        .when(pl.col('description').str.contains('NETFLIX.COM|NETFLIX|Netflix|ADOBE|ADT SECURIT')).then(pl.lit('subscriptions'))
                    # ======================= wmt =======================
        .when(pl.col('description').str.contains('WM SUPER|Wal-Mart|WAL-MART|BROOKSHIRES|BROULIM|ALBERTSONS')).then(pl.lit('wmt'))
        .when(pl.col('description').str.contains('WALGR|SMITHS|COSTCO')).then(pl.lit('wmt'))
        .when(pl.col('description').str.contains('Walmart|WALMART') &
            ~(pl.col('description').str.contains('MURPHY'))).then(pl.lit('wmt'))
                    # ======================= gas =======================
        .when(pl.col('description').str.contains('MURPHY') & 
            ~pl.col('description').str.contains('DEPOSIT|1111')).then(pl.lit('gas'))
        .when(pl.col('description').str.contains('SHELL|CHEVRON|CIRCLE K|LOVE\'S|EXXON EXPRESSWAY|EXXON MISSLE')).then(pl.lit('gas'))
        .when(pl.col('description').str.contains('MISSLE MART')).then(pl.lit('gas'))
                    # ======================= internet & phone =======================
        .when(pl.col('description').str.contains('VIASAT')).then(pl.lit('internet'))
        .when(pl.col('description').str.contains('OPTIMUM')).then(pl.lit('internet'))
        .when(pl.col('description').str.contains('VISIBLE')).then(pl.lit('internet'))
                    # ======================= shopping =======================
        .when(pl.col('description').str.contains('T J MAXX|OLD NAVY|SHEIN|REAL DEALS|SALLY BEAUTY|REXBURG DI')).then(pl.lit('shopping'))
        .when(pl.col('description').str.contains('LDS DIST ONLINE STORE|DC ULTA|DC H&amp|SEPHORA.COM|SALONCENTRIC')).then(pl.lit('shopping'))
        .when(pl.col('description').str.contains('American Eagle|SPORTSMANS WAREHOUSE|ZOE FRYE HAIR|OLDNAVY')).then(pl.lit('shopping'))
                    # ======================= amazon =======================
        .when(pl.col('description').str.contains('AMZN|AMAZON|Amazon.com|temu.com|eBay')).then(pl.lit('amazon'))
                    # ======================= fun =======================
        .when(pl.col('description').str.contains('Amazon Prime|YouTube|ZOO|MUSEUM|AQUARIUM|LION.S CLUB GOLF|PLAYSTATION NETWORK')).then(pl.lit('fun'))
        .when(pl.col('description').str.contains('COMFORT INN|CINEMA|HOLIDAY INN|El Dorado Golf|PlayStation|ROCK GYM|GRAVITY FACTORY')).then(pl.lit('fun'))
        .when(pl.col('description').str.contains('EXCALIBUR FAMILY FUN|AIRBNB|EXPEDIA|EL DORADO GOLF|UNITED|Prime Video')).then(pl.lit('fun'))
                    # ======================= power =======================
        .when(pl.col('description').str.contains('ENTERGY')).then(pl.lit('power'))
                    # ======================= car =======================
        .when(pl.col('description').str.contains('O.REILLY|MUFFLEX MUFFLER|AUTOZONE|DC TAKE 5|KARL MALONE FORD')).then(pl.lit('car'))
        .when(pl.col('description').str.contains('VAN HOOK TIRE|IRONHEART AUTOMOTIVE')).then(pl.lit('car'))
                    # ======================= progressive =======================
        .when(pl.col('description').str.contains('PROG DIRECT|STATE FARM')).then(pl.lit('progressive'))
                    # ======================= water =======================
        .when(pl.col('description').str.contains('SHARE CHECK')).then(pl.lit('water'))
        .when(pl.col('description').str.contains('EL DORADO WATER UTI|EL DORADO WATER')).then(pl.lit('water'))
                    # ======================= tithing =======================
        .when(pl.col('description').str.contains('Ch JesusChrist  DONATION|Ch JesusChrist DONATION')).then(pl.lit('tithing'))
                    # ======================= Natural Gas =======================
        .when(pl.col('description').str.contains('SUMMIT')).then(pl.lit('natural gas'))
                    # ======================= Home improvement =======================
        .when(pl.col('description').str.contains('SHERWIN-WILLIAMS|THE HOME DEPOT|MAIN STREET ANTIQUES')).then(pl.lit('home improvement'))
        .when(pl.col('description').str.contains('HOBBYLOBBY|EVERYBODYS ANTIQUE|HOBBY-LOBBY|MAIN STREET ANTIQUE')).then(pl.lit('home improvement'))
        .when(pl.col('description').str.contains('TIMMINS|Sherwin-Williams|WAYFAIR|HOMEDEPOT')).then(pl.lit('home improvement'))
                    # ======================= rent =======================
        .when((pl.col('description').str.contains('PENNYMAC'))).then(pl.lit('rent'))
        .otherwise(pl.lit('misc'))
    )


    df = df.select(['date', 'category', 'description', 'cost', 'monthName', 'month', 'day', 'year', 'weekDay', 'cardType', 'quarter'])

    # df.limit(10)

    # list(df.filter(pl.col('Category') == 'wmt')['description'].unique())
    # list(df.filter(pl.col('Category') == 'gas')['description'].unique())
    # list(df.filter(pl.col('Category') == 'unknown')['description'].unique())
    # df.sort(pl.col('cost'), descending=True).limit(20)

    return df
