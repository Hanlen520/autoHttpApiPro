import configparser
def read_email( Memail):

    config = configparser.ConfigParser()
    config.read(Memail.file, encoding='utf-8')
    Memail.report = "report.xlsx"
    Memail.to_addr = eval(config['EAMIL']['to_addr'])
    Memail.mail_host = config['EAMIL']['mail_host']
    Memail.mail_user = config['EAMIL']['mail_user']
    Memail.mail_pass =  config['EAMIL']['mail_pass']
    Memail.port = config['EAMIL']['port']
    Memail.headerMsg = config['EAMIL']['headerMsg']
    Memail.attach = config['EAMIL']['attach']
    return Memail
