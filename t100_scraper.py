import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the AI Rankings page
URL = "https://airankings.professor-x.de/?country=All&page=2&venues=all,core,AAAI,IJCAI,ECAI,Artificial%20Intelligence,JAIR,machine_learning_and_data_mining,NIPS/NeurIPS,ICML,KDD,WWW,HT,WSDM,SIGIR,COLT,ICDM,CIKM,AISTATS,SDM,ECML/PKDD,ECIR,PAKDD,RecSys,IJCNN,ICANN,ILP,ICLR,ACML,ESANN,MLJ,JMLR,IEEE%20Trans.%20Neural%20Networks,DMKD,natural_language_processing,ACL,EMNLP,NAACL,COLING,EACL,CoNLL,IJCNLP,problem_solving,ICAPS,CP,SAT,CPAIOR,SARA,SOCS,cognitive_ai,Cognitive%20Science,Cognitive%20System%20Research,Cognitive%20Processing,Topics%20in%20Cognitive%20Science,knowledge_representation,KR,AAMAS,ISWC,ESWC,CADE,LPAR,JELIA,TABLEAUX,TARK,ICLP,RuleML%20RR,ICCBR,uncertainty,UAI,Autonomous%20Agents%20and%20Multi-Agent%20Systems,AIIDE,WINE,ADT,PGM,computer_vision,CVPR,ICCV,ECCV,ACCV,TPAMI,interaction,CHI,HCI,UbiComp,IUI,UIST,robotik,RSS,IROS,Robotics%20and%20Autonomous%20Systems,IEEE%20Robotics%20and%20Automation%20Letters,Autonomous%20Robots,IJRR,ISRR,ICRA,Humanoids,CoRL,ethic_and_society,AIES"

def scrape_top_ai_authors(limit=100):
    response = requests.get(URL)
    if response.status_code != 200:
        print("Failed to fetch the AI Rankings website.")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    researchers = []
    
    # Find all table rows <tr>
    rows = soup.find_all("tr")

    # Skip the header row and extract researcher details
    for row in rows[1:]:  
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        
        name = cols[0].get_text(strip=True)
        affiliation = cols[1].get_text(strip=True)
        researchers.append({"Name": name, "Affiliation": affiliation})
        
        # Stop if we reach the limit (100)
        if len(researchers) >= limit:
            break

    return researchers

# Scrape the AI Rankings
top_authors = scrape_top_ai_authors(100)

# Convert to DataFrame
df_authors = pd.DataFrame(top_authors)

# Save to CSV
df_authors.to_csv("top_100_ai_authors.csv", index=False)

print("Top 100 AI Authors saved to 'top_100_ai_authors.csv'")
