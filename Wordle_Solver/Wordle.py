from distutils.command import check
import time
from numpy import corrcoef
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import string

winCount = 0

#initialize words with list of possible solutions for wordle
def initializeWords(words):
    #word text file needs to be refined
    with open("words.txt", "r") as a_file:
        for line in a_file:
            line = line.replace(",", " ")
            line = line.replace("[", "")
            line = line.replace("]","")
            line = line.replace('"', "")
            for w in line.split():
                words.append(w)


#send desired guess to screen 
def sendWord(driver, s, numRow):

    ActionChains(driver).send_keys(s[0]).perform()
    ActionChains(driver).send_keys(s[1]).perform()
    ActionChains(driver).send_keys(s[2]).perform()
    ActionChains(driver).send_keys(s[3]).perform()
    ActionChains(driver).send_keys(s[4]).perform()
    ActionChains(driver).send_keys(Keys.RETURN).perform()


#determine whether first row has correct letters or not then modify list of possible words
def solveRow(driver, words, numRow):

    #//*[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div/div[2]
    #//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]
    #//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]
    #//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]

    w = []
    feedback = ""
    currGuess = ""
    if numRow == 1: currGuess = "crane"
    else: currGuess = words[0]
    correct = ""
    yellow = ""

        #wait 10 seconds before looking for element
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[2]/div['+str(numRow)+']/div[1]/div/div[2]')))

    #(driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[2]/div['+str(numRow)+']/div[2]/div/div[2]'))
    #find each element
    w.append(element)
    w.append( WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[2]/div['+str(numRow)+']/div[2]/div/div[2]'))))
    w.append( WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[2]/div['+str(numRow)+']/div[3]/div/div[2]'))))
    w.append( WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[2]/div['+str(numRow)+']/div[4]/div/div[2]'))))
    w.append( WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[2]/div['+str(numRow)+']/div[5]/div/div[2]'))))

    time.sleep(3)

    #loop through all characters for word sent to screen and add to feedback
    for i in w:
        if("absent" in i.get_attribute('outerHTML')):
            feedback += "w"
        elif("present" in i.get_attribute('outerHTML')):
            feedback += "y"
            yellow += i.get_attribute('innerText').lower()
        elif("correct" in i.get_attribute('outerHTML')):
            feedback += "g"
            correct += i.get_attribute('innerText').lower()


    print(feedback)
    print(currGuess)


    #check for win with feedback
    if feedback == "ggggg":
        print("bot won after "+str(numRow)+" guesses :)")
        global winCount
        winCount += 1
        print("win number " +str(winCount))
        time.sleep(2)
        botWon(driver)
        words.clear()
        initializeWords(words)
        solve(driver, words)
        

    #create tuple because cannot iterate over a list that you want to be changed
    tempTuple = tuple(words)

    #loop through words
    for word in tempTuple:

        #loop through number of characters in word
        for i in range(5):
            #if absent letter is anywhere in word, remove
            if feedback[i] == "w" and currGuess[i] in word:
                #if letter is in correct word and it repeats then remove
                if (currGuess[i] in correct and word.count(currGuess[i]) == 1) or (currGuess[i] in yellow and word.count(currGuess[i]) == 1):
                    break
                else:
                    words.remove(word)
                break
            #if letter is correct and letter is not in same place in word, remove
            elif feedback[i] == "g" and currGuess[i] != word[i]:
                words.remove(word)
                break
            #if letter is elsewhere and letter is not anywhere in word, remove
            elif feedback[i] == "y" and currGuess[i] not in word:
                words.remove(word)
                break
            #if letter is elsewhere and letter is in same place in word, remove
            elif feedback[i] == "y" and currGuess[i] == word[i]:
                words.remove(word)
                break


#send words and narrow down words in succession
def solve(driver, words):
    sendWord(driver, "crane", 1)
    solveRow(driver, words, 1)

    while(True):
        sendWord(driver, words[0], 2)
        if checkWrongWord(driver, words, words[0], 2) == False: 
            solveRow(driver, words, 2)
            break
            
    while(True):
        sendWord(driver, words[0], 3)
        if checkWrongWord(driver, words, words[0], 3) == False: 
            solveRow(driver, words, 3)
            break

    while(True):
        sendWord(driver, words[0], 4)
        if checkWrongWord(driver, words, words[0], 4) == False: 
            solveRow(driver, words, 4)
            break

    while(True):
        sendWord(driver, words[0], 5)
        if checkWrongWord(driver, words, words[0], 5) == False: 
            solveRow(driver, words, 5)
            break
    

    while(True):
        sendWord(driver, words[0], 6)
        if checkWrongWord(driver, words, words[0], 6) == False: 
            checkLose(driver, 6, words)
            solveRow(driver, words, 6)
            break


#check to see if the bot has lost, if so exit and print how many times won
def checkLose(driver, row, words):
    global winCount
    time.sleep(2)
    ele = driver.find_element(By.CLASS_NAME, 'wp-message')
    if("The correct word was" in ele.get_attribute('innerHTML')):
        print("bot won " +str(winCount)+ " games :)")
        driver.quit()
        quit()
    else:
        print("bot won after 6 guesses :)")
        winCount += 1
        print("win number " +str(winCount))
        botWon(driver)
        words.clear()
        initializeWords(words)
        solve(driver, words)


#check to see if bot sent wrong word, if so backspace 5 times then delete that word from list and return true
def checkWrongWord(driver, words, s, row):
    ele = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[2]/div['+str(row)+']')))
    if("invalid" in ele.get_attribute('outerHTML')):
        for i in range(5): ActionChains(driver).send_keys(Keys.BACK_SPACE).perform()
        words.remove(s)
        return True
    else: return False


def botWon(driver):
    driver.find_element(By.CLASS_NAME, "btn-success").click()
        

def main():
    #initialize list of words
    words = []
    initializeWords(words)
    
    #options detach=true is so that the driver doesnt close automatically after program
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    #service is used to navigate where chromedriver is, so that chrome can be opened by selenium
    s = Service('/Users/ethaneill/Desktop/Codes/Python/chromedriver')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get("https://wordplay.com/daily")
    driver.maximize_window()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'btn-close')))

    element.click()

    solve(driver, words)

    

if __name__ == "__main__":
    main()
