def get_logo(bin):
    logo_map = {
        '860033': '/img/bank_logo/ipoteka.png',
        '860003': '/img/bank_logo/ipoteka.png',
        '860004': '/img/bank_logo/agro.png',
        '860013': '/img/bank_logo/asaka.png',
        '860009': '/img/bank_logo/qqb.png',
        '860006': '/img/bank_logo/xalq-banki.png',
        '860055': '/img/bank_logo/asia-alliance.png',
        '860049': '/img/bank_logo/kapital.png',
        '860002': '/img/bank_logo/nbu.png',
        '860005': '/img/bank_logo/mikro.png',
        '860008': '/img/bank_logo/savdogar.png',
        '860011': '/img/bank_logo/turon.png',
        '860012': '/img/bank_logo/hamkor.png',
        '860014': '/img/bank_logo/ipakyuli.png',
        '860030': '/img/bank_logo/trast.png',
        '860031': '/img/bank_logo/aloqa.png',
        '860034': '/img/bank_logo/kdb.png',
        '860038': '/img/bank_logo/turkiston.png',
        '860048': '/img/bank_logo/universalbank.png',
        '860050': '/img/bank_logo/ravnaq.png',
        '860051': '/img/bank_logo/davr-bank.png',
        '860053': '/img/bank_logo/infin.png',
        '860057': '/img/bank_logo/ofb.png',
        '860056': '/img/bank_logo/hiteck.png',
        '860020': '/img/bank_logo/ziraat.png',
        '860043': '/img/bank_logo/saderat.png',
        '860059': '/img/bank_logo/uza.png',
        '860058': '/img/bank_logo/madad.png',
        '860060': '/img/bank_logo/poytaxt.png',
        '860061': '/img/bank_logo/tenge.png',
        '986001': '/img/bank_logo/ipoteka.png',
        '986002': '/img/bank_logo/ipoteka.png',
        '986003': '/img/bank_logo/agro.png',
        '407342': '/img/bank_logo/agro.png',
        '986004': '/img/bank_logo/asaka.png',
        '986006': '/img/bank_logo/qqb.png',
        '986008': '/img/bank_logo/xalq-banki.png',
        '986009': '/img/bank_logo/asia-alliance.png',
        '986010': '/img/bank_logo/kapital.png',
        '986012': '/img/bank_logo/nbu.png',
        '986013': '/img/bank_logo/mikro.png',
        '986014': '/img/bank_logo/savdogar.png',
        '986015': '/img/bank_logo/turon.png',
        '986016': '/img/bank_logo/hamkor.png',
        '400847': '/img/bank_logo/hamkor.png',
        '986017': '/img/bank_logo/ipakyuli.png',
        '986018': '/img/bank_logo/trast.png',
        '986019': '/img/bank_logo/aloqa.png',
        '986020': '/img/bank_logo/kdb.png',
        '986021': '/img/bank_logo/turkiston.png',
        '986023': '/img/bank_logo/universalbank.png',
        '986024': '/img/bank_logo/ravnaq.png',
        '986025': '/img/bank_logo/davr-bank.png',
        '986026': '/img/bank_logo/infin.png',
        '986027': '/img/bank_logo/ofb.png',
        '986028': '/img/bank_logo/hiteck.png',
        '986029': '/img/bank_logo/ziraat.png',
        '986030': '/img/bank_logo/saderat.png',
        '986031': '/img/bank_logo/uza.png',
        '986032': '/img/bank_logo/madad.png',
        '986033': '/img/bank_logo/poytaxt.png',
        '986034': '/img/bank_logo/tenge.png',
        '986035': '/img/bank_logo/tbc.png',
        '986060': '/img/bank_logo/tbc.png',
        '4934': '/img/bank_logo/universalbank.png'
    }
    return logo_map.get(bin, 'default_logo_path')