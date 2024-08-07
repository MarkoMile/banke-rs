import pandas as pd
import math


class Agg_frame():
    dataframe_columns = [
        'Godina', 'Banka',
        'Prihodi od kamata', 'Rashodi od kamata', 'Neto prihod po osnovu kamata', 'Neto rashod po osnovu kamata',
        'Prihodi od naknada i provizija', 'Rashodi naknada i provizija', 'Neto prihod po osnovu naknada i provizija',
        'Neto rashod po osnovu naknada i provizija',
        'Neto dobitak po osnovu promene fer vrednosti finansijskih instrumenata ',
        'Neto gubitak po osnovu promene fer vrednosti finansijskih instrumenata ',
        'Neto dobitak po osnovu reklasifikacije finansijskih instrumenata',
        'Neto gubitak po osnovu reklasifikacije finansijskih instrumenata',
        'Neto dobitak po osnovu prestanka priznavanja finansijskih instrumenata koji se vrednuju po fer vrednosti',
        'Neto gubitak po osnovu prestanka priznavanja finansijskih instrumenata koji se vrednuju po fer vrednosti',
        'Neto dobitak po osnovu zaštite od rizika ', 'Neto gubitak po osnovu zaštite od rizika ',
        'Neto prihod od kursnih razlika i efekata ugovorene valutne klauzule',
        'Neto rashod od kursnih razlika i efekata ugovorene valutne klauzule',
        'Neto prihod po osnovu umanjenja obezvređenja finansijskih sredstava koja se ne vrednuju po fer vrednosti kroz bilans uspeha',
        'Neto rashod po osnovu obezvređenja finansijskih sredstava koja se ne vrednuju po fer vrednosti kroz bilans uspeha',
        'Neto dobitak po osnovu prestanka priznavanja finansijskih instrumenata koji se vrednuju po amortizovanoj vrednosti ',
        'Neto gubitak po osnovu prestanka priznavanja finansijskih instrumenata koji se vrednuju po amortizovanoj vrednosti ',
        'Neto dobitak po osnovu prestanka priznavanja investicija u pridružena društva i zajedničke poduhvate',
        'Neto gubitak po osnovu prestanka priznavanja investicija u pridružena društva i zajedničke poduhvate',
        'Ostali poslovni prihodi', 'UKUPAN NETO POSLOVNI PRIHOD', 'UKUPAN NETO POSLOVNI RASHOD',
        'Troškovi zarada, naknada zarada i ostali lični rashodi', 'Troškovi amortizacije', 'Ostali prihodi',
        'Ostali rashodi', 'DOBITAK PRE OPOREZIVANJA', 'GUBITAK PRE OPOREZIVANJA', 'Porez na dobitak ',
        'Dobitak po osnovu odloženih poreza', 'Gubitak po osnovu odloženih poreza', 'DOBITAK NAKON OPOREZIVANJA',
        'GUBITAK NAKON OPOREZIVANJA', 'Neto dobitak poslovanja koje se obustavlјa',
        'Neto gubitak poslovanja koje se obustavlјa', 'REZULTAT PERIODA - DOBITAK', 'REZULTAT PERIODA - GUBITAK',
        'Gotovina i sredstva kod centralne banke  ', 'Založena finansijska sredstva', 'Potraživanja po osnovu derivata',
        'Hartije od vrednosti', 'Krediti i potraživanja od banaka i drugih finansijskih organizacija',
        'Krediti i potraživanja od komitenata', 'Promene fer vrednosti stavki koje su predmet zaštite od rizika',
        'Potraživanja po osnovu derivata namenjenih zaštiti od rizika  ',
        'Investicije u pridružena društva i zajedničke poduhvate', 'Investicije u zavisna društva',
        'Nematerijalna imovina', 'Nekretnine, postrojenja i oprema', 'Investicione nekretnine',
        'Tekuća poreska sredstva', 'Odložena poreska sredstva',
        'Stalna sredstva namenjena prodaji i sredstva poslovanja koje se obustavlјa', 'Ostala sredstva',
        'UKUPNO AKTIVA', 'Obaveze po osnovu derivata',
        'Depoziti i ostale finansijske obaveze prema bankama, drugim finansijskim organizacijama i centralnoj banci',
        'Depoziti i ostale finansijske obaveze prema drugim komitentima',
        'Obaveze po osnovu derivata namenjenih zaštiti od rizika',
        'Promene fer vrednosti stavki koje su predmet zaštite od rizika', 'Obaveze po osnovu hartija od vrednosti',
        'Subordinirane obaveze', 'Rezervisanja',
        'Obaveze po osnovu sredstava namenjenih prodaji i sredstva poslovanja koje se obustavlјa',
        'Tekuće poreske obaveze', 'Odložene poreske obaveze', 'Ostale obaveze', 'UKUPNO OBAVEZE', 'Akcijski kapital',
        'Sopstvene akcije  ', 'Dobitak', 'Gubitak', 'Rezerve  ', 'Nerealizovani gubici', 'UKUPNO KAPITAL',
        'UKUPAN NEDOSTATAK KAPITALA', 'UKUPNO PASIVA'
    ]
    dataframe = None

    def __init__(self) -> None:
        self.dataframe = pd.DataFrame(columns=self.dataframe_columns)
        # self.dataframe

    def aggregate_bilans(self, bank_data):
        bu_columns = [
            'Godina', 'Banka',
            'Prihodi od kamata', 'Rashodi od kamata', 'Neto prihod po osnovu kamata', 'Neto rashod po osnovu kamata',
            'Prihodi od naknada i provizija', 'Rashodi naknada i provizija',
            'Neto prihod po osnovu naknada i provizija', 'Neto rashod po osnovu naknada i provizija',
            'Neto dobitak po osnovu promene fer vrednosti finansijskih instrumenata ',
            'Neto gubitak po osnovu promene fer vrednosti finansijskih instrumenata ',
            'Neto dobitak po osnovu reklasifikacije finansijskih instrumenata',
            'Neto gubitak po osnovu reklasifikacije finansijskih instrumenata',
            'Neto dobitak po osnovu prestanka priznavanja finansijskih instrumenata koji se vrednuju po fer vrednosti',
            'Neto gubitak po osnovu prestanka priznavanja finansijskih instrumenata koji se vrednuju po fer vrednosti',
            'Neto dobitak po osnovu zaštite od rizika ', 'Neto gubitak po osnovu zaštite od rizika ',
            'Neto prihod od kursnih razlika i efekata ugovorene valutne klauzule',
            'Neto rashod od kursnih razlika i efekata ugovorene valutne klauzule',
            'Neto prihod po osnovu umanjenja obezvređenja finansijskih sredstava koja se ne vrednuju po fer vrednosti kroz bilans uspeha',
            'Neto rashod po osnovu obezvređenja finansijskih sredstava koja se ne vrednuju po fer vrednosti kroz bilans uspeha',
            'Neto dobitak po osnovu prestanka priznavanja finansijskih instrumenata koji se vrednuju po amortizovanoj vrednosti ',
            'Neto gubitak po osnovu prestanka priznavanja finansijskih instrumenata koji se vrednuju po amortizovanoj vrednosti ',
            'Neto dobitak po osnovu prestanka priznavanja investicija u pridružena društva i zajedničke poduhvate',
            'Neto gubitak po osnovu prestanka priznavanja investicija u pridružena društva i zajedničke poduhvate',
            'Ostali poslovni prihodi', 'UKUPAN NETO POSLOVNI PRIHOD', 'UKUPAN NETO POSLOVNI RASHOD',
            'Troškovi zarada, naknada zarada i ostali lični rashodi', 'Troškovi amortizacije', 'Ostali prihodi',
            'Ostali rashodi', 'DOBITAK PRE OPOREZIVANJA', 'GUBITAK PRE OPOREZIVANJA', 'Porez na dobitak ',
            'Dobitak po osnovu odloženih poreza', 'Gubitak po osnovu odloženih poreza', 'DOBITAK NAKON OPOREZIVANJA',
            'GUBITAK NAKON OPOREZIVANJA', 'Neto dobitak poslovanja koje se obustavlјa',
            'Neto gubitak poslovanja koje se obustavlјa', 'REZULTAT PERIODA - DOBITAK', 'REZULTAT PERIODA - GUBITAK'
        ]
        bs_columns = [
            'Godina', 'Banka',
            'Gotovina i sredstva kod centralne banke  ', 'Založena finansijska sredstva',
            'Potraživanja po osnovu derivata', 'Hartije od vrednosti',
            'Krediti i potraživanja od banaka i drugih finansijskih organizacija',
            'Krediti i potraživanja od komitenata', 'Promene fer vrednosti stavki koje su predmet zaštite od rizika',
            'Potraživanja po osnovu derivata namenjenih zaštiti od rizika  ',
            'Investicije u pridružena društva i zajedničke poduhvate', 'Investicije u zavisna društva',
            'Nematerijalna imovina', 'Nekretnine, postrojenja i oprema', 'Investicione nekretnine',
            'Tekuća poreska sredstva', 'Odložena poreska sredstva',
            'Stalna sredstva namenjena prodaji i sredstva poslovanja koje se obustavlјa', 'Ostala sredstva',
            'UKUPNO AKTIVA', 'Obaveze po osnovu derivata',
            'Depoziti i ostale finansijske obaveze prema bankama, drugim finansijskim organizacijama i centralnoj banci',
            'Depoziti i ostale finansijske obaveze prema drugim komitentima',
            'Obaveze po osnovu derivata namenjenih zaštiti od rizika',
            'Promene fer vrednosti stavki koje su predmet zaštite od rizika', 'Obaveze po osnovu hartija od vrednosti',
            'Subordinirane obaveze', 'Rezervisanja',
            'Obaveze po osnovu sredstava namenjenih prodaji i sredstva poslovanja koje se obustavlјa',
            'Tekuće poreske obaveze', 'Odložene poreske obaveze', 'Ostale obaveze', 'UKUPNO OBAVEZE',
            'Akcijski kapital', 'Sopstvene akcije  ', 'Dobitak', 'Gubitak', 'Rezerve  ', 'Nerealizovani gubici',
            'UKUPNO KAPITAL', 'UKUPAN NEDOSTATAK KAPITALA', 'UKUPNO PASIVA'
        ]
        df_bu = pd.DataFrame(columns=bu_columns)
        df_bs = pd.DataFrame(columns=bs_columns)

        for banka, godina_dict in bank_data.items():
            for godina, tip_bilansa_dict in godina_dict.items():
                for tip_bilansa, ref_frame in tip_bilansa_dict.items():
                    if (tip_bilansa == 'BU'):
                        # drop unneeded bu 2021
                        if (godina == 2021):
                            continue
                        row = dict(zip(ref_frame.iloc[:, 1].values, ref_frame.iloc[:, 2].values))
                        row['Godina'] = godina
                        row['Banka'] = banka

                        # convert to series
                        row = pd.Series(row)

                        df_bu.loc[len(df_bu)] = row
                    elif (tip_bilansa == 'BS'):
                        row = dict(zip(ref_frame.iloc[:, 1].values, ref_frame.iloc[:, 2].values))
                        row['Godina'] = godina
                        row['Banka'] = banka

                        # convert to series
                        row = pd.Series(row)

                        df_bs.loc[len(df_bs)] = row

        # for every 2 years in df_bs, calculate average of all values
        # Sort by 'Banka' and 'Godina'
        df_bs = df_bs.sort_values(by=['Banka', 'Godina'])

        # Calculate rolling average for every 2 years
        df_bs_avg = df_bs.groupby('Banka', as_index=False).rolling(2).mean().reset_index(drop=True)

        # # Drop the first year for each bank
        df_bs_avg = df_bs_avg.groupby('Banka', as_index=False).apply(lambda x: x.iloc[1:]).reset_index(drop=True)

        # perform ceiling operation on all values in 'Godina' column
        df_bs_avg['Godina'] = df_bs_avg['Godina'].apply(lambda x: math.ceil(x))

        # Merge DataFrames on 'Godina' and 'Banka'
        self.dataframe = pd.merge(df_bu, df_bs_avg, on=['Godina', 'Banka'], how='outer', suffixes=('_bu', '_bs'))

    def print_dataframe(self):
        print(self.dataframe)

    def output_file(self, filepath):
        self.dataframe.to_excel(filepath)

    def add_indicators(self):
        yearly_total = self.dataframe.groupby('Godina')['UKUPNO AKTIVA'].transform('sum')

        interest_bearing_assets = self.dataframe['UKUPNO AKTIVA'] - self.dataframe['Nematerijalna imovina'] - \
                                  self.dataframe[
                                      'Nekretnine, postrojenja i oprema'] - self.dataframe['Investicione nekretnine'] - \
                                  self.dataframe[
                                      'Ostala sredstva']

        interest_bearing_liabilities = self.dataframe['UKUPNO OBAVEZE'] - self.dataframe[
            'Obaveze po osnovu sredstava namenjenih prodaji i sredstva poslovanja koje se obustavlјa'] - self.dataframe[
                                           'Tekuće poreske obaveze'] - self.dataframe['Odložene poreske obaveze']

        self.dataframe['Udeo na tržištu'] = (self.dataframe['UKUPNO AKTIVA'] / yearly_total) * 100

        self.dataframe['Odnos kredita prema depozitima'] = self.dataframe['Krediti i potraživanja od komitenata'] / \
                                                           self.dataframe[
                                                               'Depoziti i ostale finansijske obaveze prema drugim komitentima']
        self.dataframe['Koeficijent likvidnosti'] = (self.dataframe['Gotovina i sredstva kod centralne banke  '] / \
                                                     self.dataframe['UKUPNO AKTIVA']) * 100
        self.dataframe['Neto kamatna marža'] = self.dataframe['Neto prihod po osnovu kamata'] / interest_bearing_assets

        self.dataframe['Marža po osnovu naknada i provizija'] = (self.dataframe[
                                                                     'Neto prihod po osnovu naknada i provizija'] / interest_bearing_assets) * 100
        self.dataframe['Prosečna aktivna kamatna stopa'] = (self.dataframe[
                                                                'Prihodi od kamata'] / interest_bearing_assets) * 100

        self.dataframe['Prosečna pasivna kamatna stopa'] = (self.dataframe[
                                                                'Rashodi od kamata'] / interest_bearing_liabilities) * 100

        self.dataframe['Povrat na sopstveni kapital'] = (self.dataframe['DOBITAK PRE OPOREZIVANJA'] / self.dataframe[
            'UKUPNO KAPITAL']) * 100

        self.dataframe['Koeficijent ulaganja u hartije od vrednosti'] = (self.dataframe['Hartije od vrednosti'] / \
                                                                         self.dataframe['UKUPNO AKTIVA']) * 100

        self.dataframe['Stopa obezvređenja'] = (self.dataframe[
                                                    'Neto rashod po osnovu obezvređenja finansijskih sredstava koja se ne vrednuju po fer vrednosti kroz bilans uspeha'] / interest_bearing_assets) * 100
