import pandas
import numpy as np
import matplotlib.pyplot as plt
candidates = pandas.read_csv("1976-2020-president.csv")
# 1. Urči pořadí jednotlivých kandidátů v jednotlivých státech a v jednotlivých letech (pomocí metody rank()).
# Nezapomeň, že data je před použitím metody nutné seřadit a spolu s metodou rank() je nutné použít metodu groupby().
candidates = candidates.sort_values(["year","state"])
candidates["rank"] = candidates.groupby(["year", "state"])["candidatevotes"].rank(ascending=False)
# print(candidates.head(15))
# 2. Pro další analýzu jsou důležití pouze vítězové. Vytvoř novou tabulku, která bude obsahovat pouze vítěze voleb.
winners = candidates[candidates["rank"] == 1]
# print(winners.head(15))
# 3. Pomocí metody shift() přidej nový sloupec, abys v jednotlivých řádcích měl(a)
# po sobě vítězné strany ve dvou po sobě jdoucích letech.
winners["previous_year_winner"] = winners.groupby("state")["party_simplified"].shift(1)
# print(winners.head(15))
# 4. Porovnej, jestli se ve dvou po sobě jdoucích letech změnila vítězná strana.
# Můžeš k tomu použít např. funkci numpy.where() nebo metodu apply().
# pomocí numpy:
# winners["change"] = np.where((winners["year"] != 1976) & (winners["party_simplified"] != winners["previous_year_winner"]), 1, 0)
# pomocí apply:
def winner_change(row):
    if pandas.isnull(row["previous_year_winner"]):
        return 0
    elif row["party_simplified"] == row["previous_year_winner"]:
        return 0
    else:
        return 1
winners["change"] = winners.apply(winner_change, axis=1)
# print(winners[winners["state"] == "OHIO"])
# 5. Proveď agregaci podle názvu státu a seřaď státy podle počtu změn vítězných stran.
print(winners[winners["state"] == "OHIO"])
# states_grouped = winners.groupby("state")["change"].sum()
# states_grouped = pandas.DataFrame(states_grouped)
# states_grouped = states_grouped.sort_values("change", ascending=False)
# #print(states_grouped.head(20))
# # print(states_grouped[states_grouped["change"] == 0])
# # 6. Vytvoř sloupcový graf s 10 státy, kde došlo k nejčastější změně vítězné strany.
# # Jako výšku sloupce nastav počet změn.
# # top_10_swinging_states = states_grouped.iloc[:10]
# # top_10_swinging_states.plot(kind="bar", color="green", title="Top 10 states with most party changes")
# # Alternativně, jako více vypovídající, státy s více než 3 změnami ve sledovaném období
# top_swinging_states = states_grouped[states_grouped["change"] >= 3]
# top_swinging_states.plot(kind="bar", color="green", title="States with most party changes")
# plt.xlabel("State")
# plt.ylabel("Number of changes")
# # plt.show()