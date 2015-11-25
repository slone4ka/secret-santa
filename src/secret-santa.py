#! env python

import sys
import random
import smtplib

SMTP_ADDRESS = ''
SMTP_PASSWORD = ''
EMAIL_MESSAGE = \
    'Subject: Secret santa!\n\n' + \
    'Hello %s,\n' + \
    'You will be giving a gift to %s.'

def send_emails(participants, groups):
    smtp = smtplib.SMTP()
    smtp.connect('smtp.gmail.com', 587)
    smtp.starttls()

    try:
        smtp.login(SMTP_ADDRESS, SMTP_PASSWORD)
    except smtplib.SMTPAuthenticationError:
        print 'smtp username or password is incorrect'
        exit(1)
    except Exception as e:
        print 'an error occured while authenticating with the smtp server'
        print e
        exit(1)

    for g in groups:
        smtp.sendmail(
            SMTP_ADDRESS,
            participants[g[0]][0],
            EMAIL_MESSAGE % ( participants[g[0]][1], participants[g[1]][1] )
        )

def randomize_gifts(k):
    # k is considered the number of participants in the secret-santa
    # groups is a list which contains tuples of two integers, indices for a giver and a receiver
    idxs = range(k)
    groups = list()

    for i in range(k - 1, -1, -1):
        if i > 0:
            # more than one giver left, continue randomization
            rnd = random.randint(0, i - 1)
            g_idx = i           # the index of the current giver
            r_idx = idxs[rnd]   # random index of a receiver

            groups.append( (g_idx, r_idx) )

            aux = idxs[g_idx]
            idxs[g_idx] = idxs[rnd]
            idxs[rnd] = aux
        else:
            # only one giver left, no need for randomization
            groups.append( (0, idxs[0]) )

    return groups

def main():

    if len(sys.argv) != 2:
        print 'Usage: python secret-santa.py [emails file]'
        exit(1)

    with open(sys.argv[1], 'r') as f:
        emails = f.read()

    emails = emails.split('\n') # in windows this should be '\r\n'
    if '' in emails:
        emails.remove('')           # drop empty string

    participants = list()
    for e in emails:
        idx = e.find(' ')
        participants.append( (e[:idx], e[idx + 1:]) )

    groups = randomize_gifts( len(participants) )
    send_emails(participants, groups)

if __name__ == '__main__':
    main()
