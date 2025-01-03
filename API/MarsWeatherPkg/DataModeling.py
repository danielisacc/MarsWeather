"""Module designed to recieve data from the DB,
generate DataModels, then output the Data Models to an OutputStream."""

import matplotlib.pyplot as plt
from math import atan2, degrees
from io import BytesIO
class DataModel():
    def __init__(self, conn):
        self.conn = conn

    def getDailySummary(self, APIdata:dict) -> dict:
        latestSol = APIdata[APIdata['sol_keys'][6]]

        rightWindComponent = latestSol['WD']['most_common']['compass_right']
        upWindComponent = latestSol['WD']['most_common']['compass_up']
        windRads = atan2(rightWindComponent, upWindComponent)
        windDegrees = degrees(windRads)
        if windDegrees < 0:
            windDegrees += 360

        summaryData = {
            'sol' : APIdata['sol_keys'][6],
            'avAT' : latestSol['AT']['av'],
            'avHWS' : latestSol['HWS']['av'],
            'avPRE' : latestSol['PRE']['av'],
            'season' : latestSol['Season'],
            'mostCommonWD' : windDegrees
        }
        return summaryData

    def __loadData(self) -> int:
        if (self.conn.connect() == 200):
            self.__data = self.conn.execute("""
               SELECT sols.sol, AT.av, HWS.av, PRE.av
                FROM sols
                LEFT JOIN AT ON sols.sol = AT.sol
                LEFT JOIN HWS ON sols.sol = HWS.sol
                LEFT JOIN PRE ON sols.sol = PRE.sol""")
            return 1
        else:
            return -1

    def __renderData(self) -> int:
        if (self.__loadData()>0):
            self.__sols = [row[0] for row in self.__data]
            self.__at = [row[1] for row in self.__data if row[1] is not None]
            self.__hws = [row[2] for row in self.__data if row[2] is not None]
            self.__pre = [row[3] for row in self.__data if row[3] is not None]
            print(f"Total sols: {len(self.__sols)}, AT: {len(self.__at)}, HWS: {len(self.__hws)}, PRE: {len(self.__pre)}")
            return 1
        else:
            return -1

    def generateHistoricalGraphs(self):
        if (self.__renderData()>0):
            plt.figure(figsize=(12, 6))
            
            # Plot Atmospheric Temperature
            plt.subplot(3, 1, 1)  # 3 rows, 1 column, first subplot
            plt.plot(self.__sols, self.__at, marker='o', label='Atmospheric Temperature (°C)')
            plt.title('Atmospheric Temperature Over Martian Days')
            plt.xlabel('Martian Sol')
            plt.ylabel('Temperature (°C)')
            plt.legend()

            # Plot High Wind Speed
            plt.subplot(3, 1, 2)  # 3 rows, 1 column, second subplot
            plt.plot(self.__sols, self.__hws, marker='o', label='High Wind Speed (m/s)', color='orange')
            plt.title('High Wind Speed Over Martian Days')
            plt.xlabel('Martian Sol')
            plt.ylabel('Wind Speed (m/s)')
            plt.legend()

            # Plot Atmospheric Pressure
            plt.subplot(3, 1, 3)  # 3 rows, 1 column, third subplot
            plt.plot(self.__sols, self.__pre, marker='o', label='Atmospheric Pressure (Pa)', color='green')
            plt.title('Atmospheric Pressure Over Martian Days')
            plt.xlabel('Martian Sol')
            plt.ylabel('Pressure (Pa)')
            plt.legend()

            plt.tight_layout()  # Adjusts the spacing

            img_io = BytesIO()
            plt.savefig(img_io, format='png')  # You can change the filename and format as needed
            img_io.seek(0)

            plt.close()
            return img_io

    # Daily Summary of the weather, inlcuding max, min temp, wind speed, pressure
    # Store "Extreme" Weather events such as record Highs of temp, wind speed, or rapid pressure drops

    # Possibly create a 3d globe rendition of Mars which displays the location NASA's Insight Mission pinpointed
    # and where the sun is hitting mars in real time
