# Warning control
import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
import os
from utils import get_openai_api_key, get_serper_api_key
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Import custom scripts
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
import SERP_Get_content
import Retrieve_content_create_file

# Now environment variables are loaded
load_dotenv()

openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'

current_dir = os.path.dirname(os.path.abspath(__file__))
content_file_path = os.path.join(current_dir, "content.txt")

# Step 3: Wait for user input and content.txt file
input("Press Enter after content.txt has been created...")

try:
    with open(content_file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
except FileNotFoundError:
    print(f"找不到文件: {content_file_path}")
    print("當前工作目錄:", os.getcwd())
    raise

from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  MDXSearchTool,
  SerperDevTool
)

Researcher_Agent = Agent(
    role="Researcher_Agent",
    goal="你將專注於梳理與重組 {content} 中的內容，並依照以下指導方針進行撰寫："
         "1.標題整理：在文章開始前，先將 content.md 中的 title 提取出來並放置在文章最前，根據 title 梳理內容以確保主題連貫"
         "2.數據與引用：引用 {content} 中的任何數據、時事信息，以及與標題相關的連結，確保文章的內容具備事實基礎。"
         "3.內容清晰度：將 {content} 裡面的文字整理成方便閱讀且不失真的文章，讓文章讀起來是通順且具邏輯性的。"
         "4.編號標記：根據不同的 title，從 1 開始為每篇文章編號。"
         "5.保持專業性：梳理過程中不需添加創意元素，僅以專業的整理角度呈現內容。"
         ,

    backstory="你的任務是將 {content} 中的資料組織成一份準確無誤的參考文檔，為 SEO_Agent 提供使用基礎。"
              "請務必保持內容的真實性，避免加入 {content} 之外的連結或信息。目標讀者包括大學生、研究生、教授、上班族"
              "與高階經理人，因此文風應具備學術性及專業性，清晰且易於理解。",
    allow_delegation=False,
    verbose=True,
)


AiMochi_Knowledge = Agent(
    role="AiMochi_Knowledge",
    goal="你的任務是為 SEO_Writer 提供 AIMochi 所有服務的詳細資訊，"
         "幫助 SEO_Writer 深入了解 AIMochi 的功能及使用方法，以撰寫專業且具吸引力的文章。"
         "	1.	服務介紹：詳細解釋 AIMochi 提供的服務，包括語音轉文字、音頻轉文字、記筆記 AI、文章摘要、視頻轉文字、編輯生成的文本、多語言翻譯等。幫助 SEO_Writer 清晰理解每項服務的具體功能和用途。"
         "  2.	使用流程：說明 AIMochi 的使用流程，讓 SEO_Writer 能夠準確傳達 AIMochi 的操作步驟："
            "	•	Step 1. 加入 Line 好友：使用者可以透過此連結（https://page.line.me/aimochi?openQrModal=true）加入 AIMochi 的 Line 好友，即可獲得 1,000 點免費使用額度。"
            "  •	Step 2. 上傳錄音檔：說明如何利用 Line 的錄音功能或上傳音檔（例如會議記錄、語音紀事、YouTube 或 Podcast 網址）至 AIMochi 平台，讓系統自動轉為文字。"
            "  •	Step 3. 取得逐字稿：描述 AIMochi 的逐字稿生成流程，包括自動講者分段、智慧翻譯、逐字稿摘要與編輯功能。"
	     "  3.	保持專業性：以專業、清晰的方式整理 AIMochi 的特點，使 SEO_Writer 能撰寫針對大學生、研究生、專業人士的內容，並適合公開宣傳。",

    backstory= "AIMochi 提供多種 AI 驅動的語音與文本處理服務，旨在幫助使用者輕鬆進行文字轉錄、"
               "翻譯、摘要等。你的工作是確保 SEO_Writer 對這些服務有全面的了解，便於 SEO_Writer "
               "能夠撰寫出符合 AIMochi 品牌形象的專業 SEO 文章，並有效傳達 AIMochi 的核心價值與使用便捷性。",

    allow_delegation=False,
    verbose=True
)

SEO_Writer = Agent(
    role="SEO Writer",
    goal="你是一位專業的 SEO 寫手，每篇文章的內容長度需控制在 3000 ~ 3500 token，以詼諧幽默、雙關語、以及當下網路流行語來撰寫，"
        "打造有趣但具備專業性的 SEO 文章。文章的目標是透過 Google Search 自然流量提升讀者流量，並增強讀者對內容的參與感。為此，文章"
        "必須具備可靠的資料來源、納入與標題相關的延伸關鍵字和核心關鍵字，以提升在 Google Search 中的搜尋排名。"

        "撰寫指引："

        "1.	結構化內容：文章需具備故事性與實際案例，以吸引讀者的興趣並提供實用資訊。同時，設計 H1 ~ H5 標題架構、延伸閱讀建議、及適當的文章標籤，以數據化的方式增強 SEO 效果。"
        "2.	資料來源與連結：確保所有數據、事實均來自可靠來源，並提供可點擊的連結以供讀者進一步了解，增強內容的可信度和專業性。"
        "3.	延伸撰寫：以 Researcher_Agent 和 AIMochi_Agent 所提供的內容為基礎，針對標題進行延伸撰寫，使文章具有深度並能覆蓋相關主題。", 
    
    backstory= "你是 AiMochi 內部的資深 SEO 行銷專家，目標在於撰寫一篇具知識性和專業性的文章，旨在提供讀者豐富的資訊，而非直接推銷 AIMochi 的服務。"
               "讀者可從你文章中的連結訪問相關數據或事實來源。透過 Researcher_Agent 所整理的數據與 AIMochi_Agent 提供的服務資訊，你將編寫出一篇能"
               "解答讀者疑問且容易在搜尋引擎中被發現的文章。",

    allow_delegation=False,
    verbose=True
)

# =========================================================================================================================================================
#Create Tasks
Researcher_Bot= Task(
    description=(
        "請依照 {content} 提供的內容與標題，梳理並撰寫出結構清晰且邏輯通順的文章。你將依據以下指示來完成任務："
	    "1.在文章開頭放置 {content} 中的 title，並根據 title 梳理後續內容，使主題明確。"
        "2.引用 {content} 中提及的任何數據、時事信息及相關連結，保持內容的真實性與完整性。"
        "3.	整理內容時，確保文章易於閱讀，並符合大學生、研究生、教授、上班族和高階經理人的需求，內容應具備學術性與專業性。"
        "4.	根據每個 title 為文章編號（例如：1、2、3…），便於閱讀者區分主題。"
        "5.無需加入過多創意，僅需專業且準確地將 {content} 的內容組織為一份具邏輯性的文章。"
        "任務目標：此任務的目的是為 SEO_Agent 提供一份經過優化且真實的內容資料，方便其後續使用與參考。因此，務必保持 {content} 內容的完整性，避免添加任何未提及的外部資訊或連結。"
        "此描述旨在明確任務流程與目標，使 Researcher_Agent 能順利運行並達成既定目標。"
    ),
    expected_output="文章結構與要素："

	"1.	標題："
        "•	包含 {content} 中的 title，並在文章開頭明確顯示"
        "•	標題應反映主題，吸引讀者注意"
	"2.	主要內容整理："
        "•	文章應根據 {content} 中的數據、時事信息及相關連結，保持真實性和邏輯性"
        "•	所有引用的數據、時事或相關連結需清晰標示，且與主題有直接關聯"
        "•	各部分應按照標題順序進行編號（如 1、2、3…），方便讀者識別每個主題區塊"
	"3.	內容組織要求："
        "•	語言需具學術性與專業性，適合大學生、研究生、教授、上班族及高階經理人閱讀"
        "•	使用簡潔且通順的句子，段落結構應清晰，保證讀者易於理解"
        "•	保持內容的真實性和完整性，避免添加未經確認的外部資訊"
	"4.	文章風格與專業性："
        "•	不添加創意元素或過多情緒表達，僅以專業的整理角度呈現"
        "•	語調保持中立、清晰，以便作為 SEO_Agent 的參考基礎"
        "•	各部分之間過渡自然，內容結構緊湊，完整無誤"

    "範例輸出（以標題為例）："

        "•	標題：提升 SEO 成效的專業指南"
        "•	主要內容："
        "1.	介紹 SEO 的重要性：提供關於 SEO 對現代網路流量的影響的數據"
        "2.	核心策略概述：引用 {content} 中的數據與現有方法，詳細描述 SEO 策略的運用方法"
        "3.	實際案例分析：依據 {content} 提供的範例說明 SEO 策略的實際應用"
        "4.	總結與觀點：總結 SEO 的影響，並給予讀者深入理解的參考資料"

    "注意事項："

        "•	格式清晰：文章需條理分明，段落間以空行分隔，使內容更易於閱讀"
        "•	符合 SEO 需求：確保使用標題、次標題、及格式化的數據，符合 SEO 的結構需求"
        "•	不失真：所有引用的數據與資訊需完全忠實於 {content}，確保專業與真實性",
    agent=Researcher_Agent,
)

AIMochi_Bot = Task(
    description=(
        "你的任務是為 SEO_Writer 提供 AIMochi 服務的詳細資訊，使其能夠深入了解 AIMochi 的各項功能和使用流程。請依據以下指導方針完成任務："

        "1.	服務詳解：提供 AIMochi 所有服務的具體說明，包括語音轉文字、音頻轉文字、記筆記 AI、文章摘要、視頻轉文字、文本編輯生成、多語言翻譯等功能，並詳細解釋每項服務的用途。"
        "2.	使用步驟：清晰地描述 AIMochi 的使用流程："
            "•	Step 1. 加入 Line 好友：提供 AIMochi Line 好友連結，說明用戶加入好友即可獲得 1,000 點免費額度。"
            "•	Step 2. 上傳錄音檔：介紹使用者如何上傳音檔，包括會議記錄、YouTube 網址、Podcast 網址等，說明系統如何自動轉錄這些內容。"
            "•	Step 3. 取得逐字稿：詳細解釋 AIMochi 的逐字稿生成及智慧翻譯、摘要、編輯功能。"
        "3.	適合目標群體：撰寫內容應針對大學生、研究生、教授、上班族及高階經理人，確保內容具有專業性，能夠明確傳達 AIMochi 的價值與使用便捷性。"

        "任務目標：此任務的目的是幫助 SEO_Writer 清楚了解 AIMochi 的服務與操作步驟，便於其撰寫出具備專業性和吸引力的文章，並向讀者傳遞 AIMochi 的功能價值。"
    ),
    expected_output=    "1.	詳細服務清單：列出並解釋 AIMochi 的每項服務，強調其用途與功能，使 SEO_Writer 對各功能有全面理解。"
                        "2.	使用流程說明：分步驟介紹 AIMochi 的操作流程，每個步驟應該清晰簡明，便於 SEO_Writer 精準描述使用 AIMochi 的便捷性。"
                        "3.	專業且易讀的文字：輸出內容應條理分明，具備專業性，符合大學生、研究生、職場人士的需求，適合撰寫出一篇 SEO 優化的文章。",
    agent=AiMochi_Knowledge,
)

SEO_Writer_Bot = Task(
    description=(
        "作為一位資深的 SEO 寫手，你的目標是根據前述所提供的內容，撰寫出一篇圍繞標題的專業 SEO 文章。"
        "該文章應兼具詼諧幽默與雙關語風格，並搭配當下網路流行語，旨在吸引讀者，增強文章的參與感與分享性。同時，內容需包含延伸關鍵字及具故事性、實際案例"
        "的結構，以提高 Google Search 自然流量的搜尋機率。文章字數應控制在 3000 ~ 3500 token 之間。"
        "任務目標：提供讀者豐富的資訊與見解，建立 AIMochi 的品牌專業形象，並提高搜尋引擎上的曝光率。內容必須具備可靠的數據、參考來源，並符合 SEO 最佳實踐，提升讀者信任度。"
        "在寫完最終的 SEO 檔案後，建立一個名為 AIMochi_SEO_Article.md 的檔案，並將其儲存到目前的資料夾中。"
    ),
    expected_output = "文章結構與要素（總字數 3000 - 3500 Token）："

	"標題 (10-15字)"
        "•	必須包含關鍵字標題"
        "•	設計吸引讀者點擊的標題"
	"1. (25%)"
        "•	使用數據支持事實或與時事連結的話題的開場白或提出問題以引出標題"
        "•	介紹一個與標題相關的有趣現象或最新趨勢"
        "•	運用故事化敘述抓住讀者的注意力"
        "•	簡述文章的主要內容並暗示將介紹的解決方案"
	"2. (35%)"
        "•	透過 Researcher_Agent 和 AIMochi_Agent 的內容，提出具體案例或小故事以深入探討"
        "•	使用對比手法強調標題的關鍵價值或獨特之處"
        "•	提供與標題高度相關的連結和參考資料，增強讀者信任感"
        "•	適當使用擬人化表達，增強情感共鳴"
        "•	使用互動性提問，引導讀者參與思考"
	"3. (25%)"
        "•	將個人現象或小故事與更廣泛的社會趨勢聯繫起來"
        "•	加入社會現象解讀（15%），探討更深層次的原因或影響"
	"4. (15%)"
        "•	使用循序漸進的論證（5%）將各論點統一起來"
        "•	得出對標題的結論或提出更大的洞見"
        "•	留下思考空間或發出行動呼籲，引導讀者進行下一步"

    "注意事項："

        "•	段落結構：依循段落設計的邏輯進行撰寫。"
        "•	語氣風格：語氣詼諧幽默，使用雙關語及網路流行語，以生動有趣的方式呈現專業知識。"
        "•	文案連貫性：確保各部分之間過渡自然，故事和例子引人入勝，能引起讀者共鳴。"
        "•	語言使用：所有內容需以繁體中文（台灣）撰寫，可適當加入少量英語詞句，但主要讀者為台灣地區。",
    output_file="Expert.md",
    agent=SEO_Writer,
    )


crew = Crew(
    agents=[Researcher_Agent, AiMochi_Knowledge, SEO_Writer],
    tasks=[Researcher_Bot, AIMochi_Bot, SEO_Writer_Bot],
    verbose=2
)

result = crew.kickoff(inputs={"content": file_content})