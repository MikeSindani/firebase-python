import datetime

class AfficherAnnonce:
     def afficher(self, database):
        timeshamps = database.child("data").child("annonce").shallow().get().val()

        lis_time = []

        for i in timeshamps:
            lis_time.append(i)

        lis_time.sort(reverse=True)
        work = []
        print("test = " + str(lis_time))

        for i in lis_time:
            wor = database.child("data").child("annonce").child(i).get().val()
            work.append(wor)
        print("test2 = " + str(work))

        data = []

        for i in lis_time:
            i = float(i)
            dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M: %d-%m-%Y')
            data.append(dat)

        print(data)
        # on combine le touts
        com_list = zip(lis_time, data, work)
        return com_list