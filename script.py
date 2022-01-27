import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

fileName = input("Enter .csv file name and press ENTER:")
df = pd.read_csv(f"{fileName}.csv")
df.columns.values[0] = "trackName"
df.columns.values[1] = "artistName"
df.columns.values[3] = "playlistName"

playlistName = df['playlistName'][0]
rows = df.shape[0]


def startBrowser():
    global browser
    global window
    s = Service('./chromedriver')
    browser = webdriver.Chrome(service=s)
    window = 1


startBrowser()
print(f"{rows} tracks to download.")
for i, row in df.iterrows():

    while i+1 <= rows:
        browser.execute_script(
            '''window.open("https://free-mp3-download.net","_blank");''')
        browser.switch_to.window(browser.window_handles[window])
        window += 1
        searchField = browser.find_element(By.ID, 'q')
        searchField.send_keys(f"{row['artistName']} {row['trackName']}")
        searchField.send_keys(Keys.ENTER)

        if i+1 < rows:
            nextRow = df.iloc[i+1]
            if nextRow['playlistName'] != playlistName:
                print(f"{playlistName} done.")
                tracksLeft = rows - i
                print(f"{tracksLeft} tracks left.")
                playlistName = nextRow['playlistName']
                input(
                    f"Press Enter to continue downloading {playlistName} ...")

                tabsToClose = browser.window_handles
                tabsToClose.pop(0)
                for handle in tabsToClose:
                    browser.switch_to.window(handle)
                    browser.close()
                browser.switch_to.window(browser.window_handles[0])
                window = 1

        else:
            browser.quit()
            print("end")

        break
