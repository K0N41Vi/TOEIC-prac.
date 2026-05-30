import streamlit as st
import random
import re

# ページの設定
st.set_page_config(page_title="TOEIC Scanning Trainer", page_icon="📝", layout="centered")

# 【長時間の勉強に最適】眩しさを抑えた、淡いニュアンスカラーの洗練された北欧風UI
st.markdown("""
    <style>
    /* 1. 全体の背景とベース文字色（背景：まろやかなアイボリーホワイト / 文字：目に優しい深みのあるチャコール） */
    .stApp {
        background-color: #fcfaf7 !important;
        color: #2d2a26 !important;
    }
    
    /* 2. メインの設問タイトル（洗練された落ち着きのあるアプリコットテラコッタ） */
    h1, h2, h3, h4 {
        color: #c2410c !important;
        font-weight: 800 !important;
    }
    
    /* 3. 本文ボックス（背景：淡いミルクティーベージュ / 枠線：上品なハニーアンバー / 文字：読みやすいディープブラウン） */
    .toeic-passage-box {
        background-color: #f3ede4;
        border: 2px solid #d97706;
        padding: 26px;
        border-radius: 12px;
        line-height: 2.1;
        font-family: "Georgia", serif;
        font-size: 1.35rem;
        color: #1e1b18; /* 眩しくないけれどもしっかり読める深い焦げ茶文字 */
        word-wrap: break-word;
        white-space: pre-wrap;
        box-shadow: 0 4px 20px rgba(180, 160, 140, 0.15);
        margin-bottom: 25px;
    }
    
    /* 4. ターゲット単語バッジ（くすんだ大人のシナモンオレンジ ＋ 白文字） */
    .target-badge {
        background-color: #ea580c;
        border: 1px solid #c2410c;
        padding: 10px 20px;
        border-radius: 6px;
        color: #ffffff !important;
        font-weight: bold;
        font-size: 1.35rem;
        display: inline-block;
        margin-bottom: 15px;
        letter-spacing: 0.8px;
        box-shadow: 0 2px 8px rgba(234,88,12,0.2);
    }
    
    /* 5. ヒントや不正解時のボックス（優しいカフェラテ色 ＋ 深い焦げ茶文字） */
    .stAlert {
        background-color: #fef3c7 !important;
        color: #78350f !important;
        border: 1px solid #f59e0b !important;
    }
    
    /* 6. セレクトボックス（選択枠）の淡いトーン調整 */
    div[data-baseweb="select"] {
        border: 2px solid #d97706 !important;
        border-radius: 8px !important;
        background-color: #fbf9f6 !important;
        color: #2d2a26 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 200単語のクイズデータを完全網羅
if "question_data" not in st.session_state:
    st.session_state.question_data = [
  {
    "target_word": "Anyway",
    "theme": "プロジェクトの進捗報告",
    "passage": "To: Project Team\nFrom: Sarah Jenkins\nSubject: Project Update\n\nI am writing to inform you that there has been a slight delay in the design phase due to some technical issues with our software. We are currently working with the IT department to resolve this as quickly as possible. In any case, we are still aiming to complete the prototype by the end of this month. We might need to schedule an extra meeting next Monday to discuss the revised timeline. Please ensure your individual reports are submitted by Friday so we can stay organized. Your hard work during this busy period is greatly appreciated.",
    "question": "What is the team planning to do anyway despite the delay?",
    "paraphrased_word": "In any case",
    "explanation": "設問の「anyway（とにかく、いずれにせよ）」は、文脈を切り替えて結論を述べる際に使われます。本文中の「In any case」がこれと同じ役割を果たしており、その直後の「aiming to complete the prototype（試作機の完成を目指す）」という情報が正解の根拠となります。"
  },
  {
    "target_word": "Following",
    "theme": "セミナー後の懇親会の案内",
    "passage": "Dear Participants,\n\nThank you for registering for the 'Digital Marketing Trends' seminar held at the Grand Hotel on October 15. The main presentation will begin at 2:00 P.M. and conclude at 4:30 P.M. After the main session, there will be a networking reception in the lobby area where you can meet the speakers and other industry professionals. Refreshments and light snacks will be served during this time. Please note that parking is available at a discounted rate for all attendees. We look forward to seeing you there and hope you find the event informative and valuable for your business.",
    "question": "What will happen following the main session?",
    "paraphrased_word": "After",
    "explanation": "「following（〜の後に）」は、時系列を問う設問で頻出です。本文では「After」という単純な単語に言い換えられています。出来事の順番（プレゼン→懇親会）を整理しながら読み進めるのがポイントです。"
  },
  {
    "target_word": "Refer",
    "theme": "社内規定の確認依頼",
    "passage": "To: All Staff\nFrom: Human Resources\nSubject: New Travel Policy\n\nManagement has recently updated the company policy regarding business travel expenses. These changes will take effect starting next month. All employees are encouraged to consult the updated employee handbook for detailed information on reimbursement procedures and daily allowances. The handbook can be found on the internal company portal under the 'Documents' tab. If you have specific questions that are not addressed in the manual, please contact the HR department directly. It is important to follow these guidelines to ensure that all expense claims are processed without any delays.",
    "question": "What are employees encouraged to refer to for more details?",
    "paraphrased_word": "consult",
    "explanation": "「refer to（〜を参照する）」の言い換えとして、ビジネス文書では「consult（〜を調べる、相談する、参照する）」がよく使われます。資料やマニュアルを確認してほしいという文脈でこれらの動詞がリンクすることを予測しましょう。"
  },
  {
    "target_word": "Available",
    "theme": "会議室の予約確認",
    "passage": "Hi Mark,\n\nI checked the schedule for Conference Room B for this Wednesday. Unfortunately, it is fully booked for the entire morning. However, Room C is free between 1:00 P.M. and 3:00 P.M. if that works for your team. It has a projector and enough space for ten people. Please let me know as soon as possible if you would like to reserve it, as rooms are taken quickly. Also, remember to bring your own laptop adapter, as the room only has standard HDMI cables. I will wait for your confirmation before finalizing the booking in the system.",
    "question": "When is the conference room available on Wednesday?",
    "paraphrased_word": "free",
    "explanation": "「available（利用可能な）」は、時間や物が「空いている」ことを指します。本文中の「free（空いている）」がその言い換えです。TOEICでは人の予定や部屋の空き状況を問う際に、このペアが非常に頻繁に登場します。"
  },
  {
    "target_word": "Department",
    "theme": "異動のニュースレター",
    "passage": "We are pleased to announce that Ms. Emily Chen has been promoted to Senior Manager. Over the past five years, Emily has been an essential part of our marketing team. Starting next month, she will be moving to the sales division to lead our new international expansion project. Her extensive experience in digital strategy will be a great asset to her new colleagues. We are confident that she will continue to contribute to our company's success in this new role. Please join us in congratulating Emily on her well-deserved promotion during the coffee break in the lounge this afternoon.",
    "question": "To which department is Ms. Chen moving?",
    "paraphrased_word": "division",
    "explanation": "「department（部署）」の言い換えとして「division（部門・課）」は定番です。本文で「marketing team」から「sales division（販売部門）」への移動が述べられている箇所を探し出します。"
  },
  {
    "target_word": "Conference",
    "theme": "業界イベントへの参加案内",
    "passage": "Subject: Upcoming Industry Event\n\nDear Members,\n\nRegistration is now open for the Annual Technology Convention, which will be held in San Francisco this year. This event is a great opportunity to learn about the latest innovations in software development and network with experts from around the world. There will be over 50 workshops and keynote speeches by industry leaders. Early-bird registration is available until the end of this month, offering a 20% discount on the entry fee. We highly recommend attending this gathering to stay updated on current trends. For more details on the schedule and guest speakers, please visit our official website.",
    "question": "What is the purpose of the conference in San Francisco?",
    "paraphrased_word": "Convention",
    "explanation": "設問の「conference（会議）」に対し、本文では「Convention（大会、コンベンション）」が使われています。大規模な会議やイベントを指す際、これらはほぼ同じ意味で交換可能です。"
  },
  {
    "target_word": "According to",
    "theme": "市場調査の結果報告",
    "passage": "The latest quarterly report shows a significant increase in consumer interest in eco-friendly products. As stated in the survey conducted last month, nearly 70% of our customers prefer to buy items with recyclable packaging. This trend is particularly strong among younger shoppers aged 18 to 30. In response to these findings, we plan to adjust our product line to include more sustainable options by next spring. Our marketing strategy will also focus more on highlighting our environmental initiatives. We believe this shift will help us maintain our competitive edge in the changing market and attract more environmentally conscious buyers.",
    "question": "According to the survey, what do customers prefer?",
    "paraphrased_word": "As stated in",
    "explanation": "「According to（〜によれば）」は情報の出所を示すフレーズです。本文の「As stated in（〜に述べられている通り）」がその根拠を示す合図になっています。"
  },
  {
    "target_word": "Likely",
    "theme": "天候による配送遅延の予測",
    "passage": "Due to a severe winter storm approaching the East Coast, we expect that some shipments may experience delays over the next few days. Our logistics team is working hard to minimize the impact on our customers. It is probable that deliveries scheduled for Thursday and Friday will arrive at least 24 hours late. We recommend checking your tracking number on our website for real-time updates on your package's status. We apologize for any inconvenience caused by these weather conditions beyond our control. Thank you for your understanding and patience as we prioritize the safety of our drivers.",
    "question": "What is likely to happen to shipments this week?",
    "paraphrased_word": "probable",
    "explanation": "「likely（〜しそうだ、可能性が高い）」という推測を表す語は、本文で「probable（ありそうな、見込みの）」と言い換えられます。"
  },
  {
    "target_word": "Offer",
    "theme": "新規顧客向けのキャンペーン",
    "passage": "Welcome to Sparkle Fitness Center! To celebrate our fifth anniversary, we are excited to provide a special discount to all new members who sign up this week. If you join by Friday, you will receive a 50% discount on the first three months of your membership. Additionally, we are including a free personal training session to help you get started on your fitness journey. Our facilities feature state-of-the-art gym equipment and a variety of group classes, including yoga and pilates. Don't miss this chance to improve your health at a great price. Visit our front desk today for more information.",
    "question": "What does the fitness center offer to new members?",
    "paraphrased_word": "provide",
    "explanation": "「offer（提供する）」は、サービスや特典について述べる際によく使われます。本文の「provide（提供する）」が対応する語です。"
  },
  {
    "target_word": "Equipment",
    "theme": "新しいオフィスの備品導入",
    "passage": "Our office relocation to the downtown area is almost complete. To ensure a productive work environment, the company has invested in high-quality office machinery for the new space. Each workstation will be equipped with dual monitors and ergonomic chairs. Furthermore, the communal kitchen has been upgraded with a new espresso maker and a larger refrigerator. Please note that training sessions on how to use the new multi-function printers will be held next Tuesday morning. All staff members are required to attend one of the 20-minute sessions. We hope these new tools will make your daily tasks easier and more efficient.",
    "question": "What kind of equipment will be available at the new office?",
    "paraphrased_word": "machinery",
    "explanation": "「equipment（機器、備品）」の広義の言い換えとして「machinery（機械類）」が使われています。具体的なアイテムを総称する語を探す訓練です。"
  },
  {
    "target_word": "Provide",
    "theme": "フィードバックの依頼",
    "passage": "Thank you for attending the annual leadership workshop yesterday. We hope you found the sessions helpful and inspiring. To help us improve future events, we would like to ask you to give us your feedback regarding the speakers and the venue. Please click the link below to complete a short online survey, which should take no more than five minutes of your time. Your comments are very important to us and will be used to plan our next training program. As a token of our appreciation, participants who complete the survey will be entered into a prize draw for a gift card.",
    "question": "What are participants asked to provide?",
    "paraphrased_word": "give us your feedback",
    "explanation": "本文では「give us your feedback（フィードバックをくれる）」という表現が、設問の「provide feedback」に相当します。"
  },
  {
    "target_word": "Local",
    "theme": "地域密着型の店舗宣伝",
    "passage": "At 'Green Groceries,' we take pride in supporting our community. That is why 90% of our fruits and vegetables are sourced from nearby farms within a 50-mile radius. By choosing to shop with us, you are helping to reduce transportation emissions and supporting small businesses in the area. This week, we have a fresh arrival of organic strawberries and honey. Our store is open daily from 8:00 A.M. to 9:00 P.M. for your convenience. Stop by and taste the difference that fresh, regional produce can make. We look forward to serving you and your family with the best quality goods.",
    "question": "Where does the store get its local produce?",
    "paraphrased_word": "nearby",
    "explanation": "「local（地元の）」という言葉は、本文で「nearby（近くの）」や「in the area」と言い換えられるのが一般的です。"
  },
  {
    "target_word": "Purchase",
    "theme": "オンラインショップの確認メール",
    "passage": "Dear Customer,\n\nThank you for choosing TechWorld for your electronic needs. This email is to confirm that we have received your order #44592. You chose to buy a wireless keyboard and a noise-canceling headset. Your items are currently being processed in our warehouse and will be shipped via express courier tomorrow morning. You will receive another notification with a tracking number once the package is on its way. Please review the attached invoice to ensure your billing information is correct. If you notice any errors, please contact our customer support team immediately to make changes before shipment.",
    "question": "What items did the customer purchase?",
    "paraphrased_word": "buy",
    "explanation": "「purchase（購入する）」はフォーマルな語で、日常的な「buy（買う）」の言い換えとして定番です。"
  },
  {
    "target_word": "Opening",
    "theme": "新規店舗の開店告知",
    "passage": "Grand Unveiling of Blue Wave Cafe!\n\nWe are excited to announce that Blue Wave Cafe will be welcoming its first customers this Saturday at 10:00 A.M. Located on the corner of Oak Street and 5th Avenue, our cafe offers a cozy atmosphere and the finest organic coffee beans. To celebrate our first day, we will be offering a 'buy one, get one free' deal on all beverages until noon. There will also be live music performed by a local jazz band. Come and explore our delicious menu of homemade pastries and sandwiches. We can't wait to become a part of this vibrant neighborhood and meet our new neighbors.",
    "question": "Grand Unveiling of Blue Wave Cafe!",
    "paraphrased_word": "Unveiling",
    "explanation": "「opening（開店、開始）」はタイトルの「Unveiling（初披露）」という表現で示されています。"
  },
  {
    "target_word": "Construction",
    "theme": "道路工事の通知",
    "passage": "Public Notice: Road Maintenance on West Street\n\nStarting Monday, November 12, there will be significant building work occurring near the intersection of West Street and Miller Road. This project is part of the city's plan to improve underground water pipes and resurface the road. As a result, certain lanes will be closed during the day, and traffic may be slower than usual. Drivers are advised to use alternative routes if possible to avoid delays. The project is expected to be completed within two weeks, weather permitting. We apologize for the temporary noise and inconvenience this essential work may cause to residents and local business owners.",
    "question": "How long will the construction project last?",
    "paraphrased_word": "building work",
    "explanation": "「construction（建設、工事）」は「building work」という言葉で本文に現れることがあります。"
  },
  {
    "target_word": "Tour",
    "theme": "歴史的建造物の見学ツアー",
    "passage": "Join us for a guided site visit of the historic City Hall building. These sessions are held every Saturday afternoon at 2:00 P.M. and 4:00 P.M. During the 45-minute walk, a knowledgeable guide will share fascinating stories about the architecture and the city's political history. You will have the chance to see the mayor's office and the beautifully restored council chamber. Tickets are $10 for adults and $5 for students and seniors. Due to limited group sizes, we recommend booking your spot in advance through our website. Please arrive at the main entrance ten minutes before the scheduled start time.",
    "question": "How long does the tour of City Hall last?",
    "paraphrased_word": "site visit",
    "explanation": "「tour（見学、ツアー）」は、施設を訪れるという意味で「site visit」と言い換えられます。"
  },
  {
    "target_word": "Research",
    "theme": "新製品開発の調査報告",
    "passage": "The development team has completed its initial investigation into new battery technologies for our upcoming smartphone model. The study focused on increasing battery life while reducing charging time. Our engineers found that using a new type of lithium-ion compound could improve efficiency by 15%. However, further testing is needed to ensure the stability of the materials under high temperatures. We plan to conduct more trials over the next three months before finalizing the design. The results so far are very promising, and we are optimistic about the impact this will have on our market share. A full report will be presented at the board meeting.",
    "question": "What was the main focus of the research?",
    "paraphrased_word": "investigation",
    "explanation": "「research（調査、研究）」は「investigation（調査、検分）」と言い換えられます。"
  },
  {
    "target_word": "Attend",
    "theme": "トレーニング研修への参加",
    "passage": "To: All Project Managers\nFrom: Director of Operations\n\nA mandatory training session on the new project management software will be held on Wednesday, June 5. All managers are required to participate in this workshop to learn about the new features and reporting tools. The session will take place in the main conference room from 9:00 A.M. to 12:00 P.M. Please bring your company laptops so you can follow along with the practical exercises. If you are unable to go to the meeting due to a prior commitment, please notify your supervisor as soon as possible to arrange a one-on-one catch-up session at a later date.",
    "question": "Who is required to attend the training session?",
    "paraphrased_word": "participate in",
    "explanation": "「attend（出席する）」は「participate in（参加する）」に言い換えられます。"
  },
  {
    "target_word": "Delivery",
    "theme": "商品の配送遅延通知",
    "passage": "Dear Mr. Thompson,\n\nWe are writing to update you on the status of your recent furniture order. Unfortunately, due to a delay at our manufacturing plant, the shipment of your dining table has been rescheduled. We now expect it to arrive at your address on Friday, July 12, instead of the original date. Our local carrier will call you on the morning of the arrival to confirm a specific time window for the drop-off. We understand this delay may be inconvenient and would like to offer you a 10% discount on your next purchase as an apology. Thank you for choosing HomeStyles Furniture.",
    "question": "When is the new delivery date for the dining table?",
    "paraphrased_word": "shipment",
    "explanation": "「delivery（配達）」は物流の文脈では「shipment（発送品、出荷）」と言い換えられます。"
  },
  {
    "target_word": "Recently",
    "theme": "新社長就任の発表",
    "passage": "The Board of Directors is pleased to announce the appointment of Ms. Linda Foster as the new CEO of Global Solutions. Lately, the company has undergone several major changes to improve its international operations, and Ms. Foster's leadership is expected to drive further growth. She has over 20 years of experience in the telecommunications industry and previously served as the Chief Operating Officer at NexaCorp. Ms. Foster will officially begin her new role on January 1. She will be visiting each regional office over the next month to meet with staff and discuss her vision for the company's future. Please join us in welcoming her.",
    "question": "What has the company done recently?",
    "paraphrased_word": "Lately",
    "explanation": "「recently（最近）」の言い換えとして「Lately」は非常によく使われます。"
  },
  {
    "target_word": "Policy",
    "theme": "新しいリモートワーク規定",
    "passage": "To all staff, please be advised that the company has updated its internal guidelines regarding flexible working hours. These new rules will take effect starting next month. Employees are now permitted to work from home two days a week, provided they coordinate with their department heads in advance. The aim of this change is to improve work-life balance and increase overall productivity. Please review the document attached to this email for full details on eligibility and reporting procedures. If you have any specific questions about how these regulations apply to your team, please contact the Human Resources department during regular office hours. Thank you for your continued hard work and cooperation.",
    "question": "What is the purpose of the new company policy?",
    "paraphrased_word": "guidelines",
    "explanation": "設問の「policy（規定、方針）」は、本文では「guidelines（指針）」と言い換えられています。"
  },
  {
    "target_word": "Register",
    "theme": "スキルアップ講座の申し込み",
    "passage": "Are you interested in improving your public speaking skills? Join our upcoming workshop, 'Effective Presentations,' held on October 20. This session is designed for professionals who want to communicate with confidence. Space is limited to 15 participants to ensure everyone gets personalized feedback. To sign up for the event, please visit the staff portal and complete the online form by this Friday. A registration fee of $50 will be charged to your department's training budget. Don't miss this chance to learn from industry experts and network with colleagues from different departments. We look forward to helping you grow your professional capabilities.",
    "question": "How can employees register for the workshop?",
    "paraphrased_word": "sign up",
    "explanation": "「register（登録する、申し込む）」の最も一般的な言い換えは「sign up」です。"
  },
  {
    "target_word": "Arrange",
    "theme": "出張の宿泊手配",
    "passage": "Dear Ms. Miller, I am writing to confirm that I have organized your accommodation for the conference in Singapore next week. I have booked a room at the Grand Plaza Hotel, which is only a five-minute walk from the convention center. Your stay includes breakfast and access to the business lounge. I have also scheduled a shuttle service to pick you up from the airport upon your arrival. Please find the itinerary and hotel confirmation number attached. If you need to make any changes to these plans, please let me know by Wednesday so I can contact the travel agency. Have a safe and productive trip.",
    "question": "What has the sender managed to arrange for Ms. Miller?",
    "paraphrased_word": "organized",
    "explanation": "「arrange（手配する）」は、ビジネスの文脈では「organize（準備する、組織する）」と言い換えられます。"
  },
  {
    "target_word": "Bill",
    "theme": "支払明細の誤りに関する問い合わせ",
    "passage": "Dear Customer Service, I am writing regarding the recent invoice I received for my monthly internet service. According to the statement, I have been charged $85, but my contracted monthly rate is only $60. It appears that an extra fee for equipment rental was added to my account by mistake, even though I use my own router. Could you please review my records and issue a corrected document? I have attached a copy of my original contract for your reference. I would appreciate it if this matter could be resolved before the payment due date. Thank you for your assistance.",
    "question": "What is the problem with the monthly bill?",
    "paraphrased_word": "invoice",
    "explanation": "「bill（請求書）」は、ビジネス文書では「invoice（請求書）」と言い換えられます。"
  },
  {
    "target_word": "Hire",
    "theme": "新規スタッフの採用告知",
    "passage": "We are excited to announce that we plan to recruit three new account managers to support our growing client base. Since we expanded our operations into the European market, our workload has increased significantly. The ideal candidates should have at least three years of experience in sales and be fluent in at least two languages. We will be posting the job descriptions on our website and major social media platforms later this week. If you know anyone who might be a good fit for these roles, please encourage them to apply. We hope to have the new team members start by the beginning of the next quarter.",
    "question": "Why does the company need to hire new managers?",
    "paraphrased_word": "recruit",
    "explanation": "「hire（雇う）」は、採用活動 of の文脈では「recruit（募集する、採用する）」と言い換えられます。"
  },
  {
    "target_word": "Approve",
    "theme": "予算の承認",
    "passage": "To: Marketing Team\nFrom: Financial Director\nSubject: Campaign Budget\n\nI have reviewed the proposal for the upcoming summer advertising campaign. I am pleased to inform you that the board has decided to authorize the full requested budget of $50,000. We were particularly impressed by your focus on digital platforms and social media influencers. You may begin contacting the vendors and finalized the contracts immediately. Please ensure that all expenditures are tracked carefully and reported in our monthly meetings. We have high expectations for this campaign and look forward to seeing the results. Good luck with the implementation.",
    "question": "Who had the authority to approve the budget?",
    "paraphrased_word": "authorize",
    "explanation": "「approve（承認する）」は許可を出す意味の「authorize（認可する）」と言い換えられます。"
  },
  {
    "target_word": "Conduct",
    "theme": "従業員満足度調査の実施",
    "passage": "To improve our workplace environment, the HR department will carry out an anonymous survey starting next Monday. This initiative aims to gather honest feedback regarding office facilities, management support, and career development opportunities. All employees are encouraged to participate, as your opinions are vital for our future growth. The survey will take approximately ten minutes to complete and can be accessed via the link sent to your corporate email. Please submit your responses by Friday evening. We will share a summary of the findings and our planned improvements during the general staff meeting next month. Thank you for your time.",
    "question": "What is the company planning to conduct?",
    "paraphrased_word": "carry out",
    "explanation": "「conduct（実施する）」は、調査や研究の文脈で句動詞の「carry out」に頻繁に言い換えられます。"
  },
  {
    "target_word": "Opportunity",
    "theme": "海外研修のチャンス",
    "passage": "At Sterling Consulting, we believe in investing in our employees' professional growth. We are currently offering a unique chance for junior consultants to spend three months working at our London branch. This program allows participants to gain international experience and learn about global financial markets firsthand. To be eligible, you must have completed at least one year with the firm and have a strong performance record. Interested individuals should submit a letter of interest and a recommendation from their supervisor by the end of the month. This is a fantastic way to expand your professional network and develop new skills.",
    "question": "What kind of opportunity is available for junior consultants?",
    "paraphrased_word": "chance",
    "explanation": "「opportunity（機会、チャンス）」は、日常的な単語「chance」に言い換えられます。"
  },
  {
    "target_word": "Deadline",
    "theme": "報告書の提出期限",
    "passage": "Attention all project leads: Please remember that the final quarterly reports must be submitted by 5:00 P.M. this Thursday. This due date is firm because the information needs to be compiled for the board meeting on Monday. If you anticipate any issues in meeting this requirement, please contact your supervisor immediately to discuss a solution. Ensure that all data tables are accurate and that the executive summary is clearly written. Reports should be uploaded to the shared drive in PDF format. We appreciate your efforts in providing this information on time to ensure a smooth reporting process for the entire organization.",
    "question": "When is the deadline for submitting the reports?",
    "paraphrased_word": "due date",
    "explanation": "「deadline（締切）」の言い換えとして「due date（期日）」は定番です。"
  },
  {
    "target_word": "Corporate",
    "theme": "企業イメージの刷新",
    "passage": "In order to better reflect our vision for the future, we are launching a new company-wide branding initiative. This project involves updating our logo, website design, and marketing materials. We want to create a more modern and professional image that resonates with our international clients. As part of this process, we will also be updating our business cards and letterheads. A presentation explaining the new brand identity will be held in the auditorium this Friday morning. All staff members are encouraged to attend. We believe this new look will strengthen our position in the industry and represent our commitment to innovation and quality.",
    "question": "What is the focus of the new corporate initiative?",
    "paraphrased_word": "company-wide",
    "explanation": "「corporate（企業の）」は、組織全体を指す「company-wide（全社的な）」と言い換えられます。"
  },
  {
    "target_word": "Warranty",
    "theme": "製品保証による修理",
    "passage": "Thank you for contacting our support team regarding your recent purchase. All of our electronic products come with a two-year guarantee that covers manufacturing defects and hardware failures. Based on the photos you sent, it appears your tablet's screen issue qualifies for a free repair. Please send the device to our service center using the prepaid shipping label attached to this email. Make sure to back up your data before shipping, as the device may be reset during the service process. Once we receive the item, our technicians will examine it and complete the necessary work within five business days. We apologize for any inconvenience.",
    "question": "What does the warranty cover for the tablet?",
    "paraphrased_word": "guarantee",
    "explanation": "「warranty（保証）」は「guarantee（保証）」と言い換えられます。"
  },
  {
    "target_word": "Necessary",
    "theme": "入館に必要な手続き",
    "passage": "To maintain high security standards, all visitors to our headquarters must follow certain procedures. It is essential to present a valid photo ID, such as a driver's license or passport, at the reception desk upon arrival. Visitors will then be issued a temporary security badge, which must be worn visibly at all times while inside the building. Please note that guests must be accompanied by a staff member when entering restricted areas, such as the data center or laboratory. We recommend that employees inform the security office at least 24 hours in advance when expecting outside guests to ensure a smooth check-in process for everyone involved.",
    "question": "What is necessary for visitors to show at the reception?",
    "paraphrased_word": "essential",
    "explanation": "「necessary（必要な）」は、フォーマルな文脈では「essential（不可欠な、必須の）」と言い換えられます。"
  },
  {
    "target_word": "Reserve",
    "theme": "レストランの予約",
    "passage": "Are you planning a business lunch or a special celebration? At 'The Oak Room,' we offer private dining areas that can accommodate groups of up to 20 people. To book a table for your next event, please use our online system or call us directly. We recommend making your arrangements at least two weeks in advance, especially for weekend bookings. Our menu features seasonal ingredients sourced from local farms, and we can also provide customized catering options to meet your specific dietary requirements. We look forward to providing you and your guests with an exceptional dining experience and high-quality service in a sophisticated atmosphere.",
    "question": "How far in advance should customers reserve a table for a group?",
    "paraphrased_word": "book",
    "explanation": "「reserve（予約する）」の最も一般的な言い換えは「book」です。"
  },
  {
    "target_word": "Resident",
    "theme": "マンションの配管工事通知",
    "passage": "Attention all building occupants: This is to inform you that maintenance work on the main water pipes will be carried out this Wednesday, May 15. As a result, the water supply will be temporarily unavailable between 10:00 A.M. and 2:00 P.M. We advise you to store enough water for your needs during this period. We apologize for any inconvenience this essential maintenance may cause and appreciate your understanding. Our team will work as quickly as possible to restore service before the scheduled time. If you have any questions or experience any issues after the work is completed, please contact the building manager's office immediately.",
    "question": "Who is the notice for regarding the residents?",
    "paraphrased_word": "occupants",
    "explanation": "「resident（居住者）」は、建物の利用者を指す「occupant（占有者、居住者）」と言い換えられます。"
  },
  {
    "target_word": "Create",
    "theme": "新製品の開発",
    "passage": "Our research and development team is working hard to develop a more energy-efficient battery for our next generation of electric vehicles. By using advanced materials, we aim to increase the driving range by 30% while reducing charging time. This project is a key part of our commitment to sustainability and innovation. We expect to begin testing the first prototypes by the end of the year. If the trials are successful, we will start mass production by next summer. This new technology will help us stay ahead of our competitors and provide our customers with more reliable and environmentally friendly transportation options. We are excited about the potential impact of this project.",
    "question": "What is the team trying to create?",
    "paraphrased_word": "develop",
    "explanation": "「create（作り出す）」は、製品や技術の文脈では「develop（開発する）」と言い換えられます。"
  },
  {
    "target_word": "Inform",
    "theme": "スケジュールの変更通知",
    "passage": "Dear Participants, we would like to notify you that the location of tomorrow's 'Modern Architecture' seminar has been changed. Due to an unexpected plumbing issue in Hall A, the session will now take place in the Skyview Lounge on the 10th floor. The starting time remains the same at 10:00 A.M. We have updated the signage in the lobby to help you find the new venue. We apologize for the last-minute change and any confusion this may cause. If you have any trouble finding the room, please ask the staff at the information desk for assistance. We look forward to an engaging and informative session with you all.",
    "question": "What does the sender want to inform the participants about?",
    "paraphrased_word": "notify",
    "explanation": "「inform（知らせる）」は、通知や連絡の文脈で「notify（通知する）」と言い換えられます。"
  },
  {
    "target_word": "Allow",
    "theme": "オフィスの入館許可",
    "passage": "To improve safety, the new electronic keycard system will permit access only to authorized personnel after 7:00 P.M. Employees who need to work late must ensure they have their updated security badges. If you have lost your badge, please contact the security office immediately for a replacement. Visitors are not allowed in the building during these hours unless they have a pre-arranged appointment and are accompanied by a staff member. We believe these measures are necessary to protect our sensitive data and equipment. We appreciate your cooperation in following these new security protocols to ensure a safe working environment for everyone.",
    "question": "What will the new keycard system allow employees to do?",
    "paraphrased_word": "permit access",
    "explanation": "「allow（許す）」は、アクセス権の文脈で「permit（許可する）」と言い換えられます。"
  },
  {
    "target_word": "Mention",
    "theme": "顧客からのフィードバック",
    "passage": "Thank you for providing your feedback on our new software interface. We were glad to hear that the layout is intuitive and easy to navigate. In your comments, you also indicated that the loading speed could be improved for larger files. We have shared this observation with our technical team, and they are currently working on an update to optimize performance. Your input is valuable to us as we strive to create the best user experience possible. We will notify you once the new version is available for download. As a token of our appreciation, we have added a 10% discount coupon to your account for your next subscription renewal.",
    "question": "What did the customer mention in the feedback?",
    "paraphrased_word": "indicated",
    "explanation": "「mention（述べる）」は、意見を伝える意味の「indicate（〜を指し示す、述べる）」と言い換えられます。"
  },
  {
    "target_word": "Appreciate",
    "theme": "ボランティアへの感謝",
    "passage": "Dear Volunteers, we would like to express our gratitude for your help during last weekend's community tree-planting event. Because of your hard work and dedication, we were able to plant over 200 young trees in the local park. This effort will significantly improve the air quality and beauty of our neighborhood for years to come. We value the time and energy you contributed to this cause. We will be hosting a small appreciation lunch this Saturday at the community center to say thank you properly. Please let us know if you can attend by Wednesday so we can finalize the catering. We hope to see you there and celebrate our collective success.",
    "question": "Why does the organization appreciate the volunteers?",
    "paraphrased_word": "value",
    "explanation": "「appreciate（感謝する、価値を認める）」は「value（〜を重んじる、評価する）」と言い換えられます。"
  },
  {
    "target_word": "Replacement",
    "theme": "故障品の交換対応",
    "passage": "Dear Mr. Kim, we received your report regarding the damaged coffee maker you purchased from our online store. We apologize for the condition in which the item arrived. We have already shipped a substitute unit to you via express courier, and it should arrive at your doorstep within two days. You do not need to return the faulty item; please dispose of it according to your local recycling regulations. We have also included a small gift as a gesture of goodwill for the inconvenience. Our goal is to ensure all our customers receive high-quality products. If you have any further questions, please do not hesitate to contact us. Thank you for your patience.",
    "question": "What is the company sending as a replacement for the damaged item?",
    "paraphrased_word": "substitute",
    "explanation": "「replacement（交換品）」は、物流の文脈では「substitute（代替品）」と言い換えられます。"
  },
  {
    "target_word": "Update",
    "theme": "ソフトウェア更新通知",
    "passage": "Dear Users, we are releasing a revised version of the SparkMail application this Friday. This modification is designed to fix several bugs reported by our customers and to improve the overall security of your data. The installation process will take approximately ten minutes, during which the service may be temporarily unavailable. We strongly recommend that you install this latest edition as soon as it becomes available to ensure your account remains protected. Detailed instructions on how to perform the installation can be found on our support page. Thank you for choosing SparkMail.",
    "question": "What is the main purpose of the software update?",
    "paraphrased_word": "revised version",
    "explanation": "「update（更新）」は、本文では「revised version（改訂版）」と言い換えられています。"
  },
  {
    "target_word": "Branch",
    "theme": "新店舗のオープン告知",
    "passage": "Sunny Coffee is proud to announce the opening of its newest local office in the downtown shopping district. This will be our fifth location in the city, and it will feature an expanded menu of organic teas and handmade pastries. To celebrate our grand opening this Saturday, we are offering a 20% discount on all large beverages until noon. Our goal is to provide a comfortable space for students and professionals alike to relax and enjoy premium coffee. We invite everyone in the neighborhood to visit our new site and meet our friendly baristas. Free Wi-Fi and ample seating are available.",
    "question": "Where is the new branch located?",
    "paraphrased_word": "local office",
    "explanation": "「branch（支店）」は、ビジネスの文脈で「local office（現地的のオフィス）」と言い換えられます。"
  },
  {
    "target_word": "Paid",
    "theme": "請求書の支払い確認",
    "passage": "To: Jennifer Lopez\nFrom: Billing Department\nSubject: Payment Confirmation\n\nDear Ms. Lopez, this email is to confirm that we have received your transaction for Invoice #9938. Your balance has been fully settled as of July 15. We appreciate your promptness in addressing this matter. Your current subscription to our cloud storage service will now remain active until the next billing cycle in January. If you would like to view your transaction history or download a PDF copy of your receipt, please log in to your account portal and navigate to the 'Finance' tab. If you have any further questions, please contact our support team. Thank you.",
    "question": "Has the invoice for the cloud storage been paid?",
    "paraphrased_word": "settled",
    "explanation": "「paid（支払われた）」の言い換えとして、未払い金などが解決したことを示す「settled（精算された）」が使われます。"
  },
  {
    "target_word": "Unfortunately",
    "theme": "イベント中止の連絡",
    "passage": "Dear Ticket Holders,\nWe regret to inform you that the outdoor concert scheduled for this Saturday has been canceled due to a forecast of heavy rain and thunderstorms. Regrettably, the event cannot be rescheduled this season because of the band's busy touring schedule. Full refunds will be automatically issued to the original credit card used for the purchase within seven business days. We apologize for the disappointment this may cause and appreciate your understanding. Please check our website for information on future performances and upcoming ticket sales. Thank you for your continued support of local live music.",
    "question": "Why is the concert, unfortunately, not going to happen?",
    "paraphrased_word": "Regrettably",
    "explanation": "「unfortunately（残念ながら）」は、悪いニュースを伝える際の副詞「Regrettably」に言い換えられます。"
  },
  {
    "target_word": "Original",
    "theme": "初期デザイン案の変更",
    "passage": "During the meeting yesterday, the creative team discussed the feedback regarding the initial proposal for the new brand logo. While the client liked the overall concept, they suggested that we change the color palette to more earthy tones. We have decided to keep the font from the first version but will modify the background graphics to look more modern. These changes aim to better reflect the company's commitment to sustainability. Please review the updated drafts by Wednesday afternoon. If you have any strong opinions on the revised icons, let the project lead know before we finalize the presentation for the board members.",
    "question": "What will happen to the original logo proposal?",
    "paraphrased_word": "initial",
    "explanation": "「original（最初の）」は、プロジェクトの初期段階を指す「initial」と言い換えられます。"
  },
  {
    "target_word": "Rent",
    "theme": "オフィスの賃貸料改定",
    "passage": "Dear Tenants,\nPlease be advised that there will be a slight increase in the monthly lease payment starting in October. This adjustment is necessary to cover the rising costs of building maintenance and security services. We remain committed to providing a high-quality working environment for all our clients. The new rate will be $2,500 per month for all standard office units. Please update your automatic payment settings to reflect this change. If you have any questions regarding the terms of your contract, please feel free to reach out to the management office. We value your presence in our building and appreciate your cooperation.",
    "question": "How much will the rent be starting in October?",
    "paraphrased_word": "lease payment",
    "explanation": "「rent（賃貸料）」は「lease payment（リース料、賃貸支払い）」と言い換えられます。"
  },
  {
    "target_word": "Memo",
    "theme": "社内規定に関する連絡",
    "passage": "To: All Employees\nFrom: Office Management\n\nPlease read this internal message carefully regarding the new recycling procedures in the breakroom. Starting Monday, we will be using separate bins for plastics, paper, and organic waste. This initiative is part of our ongoing effort to reduce the company's environmental footprint. We ask that all staff members follow the labels on the containers to ensure proper sorting. Failure to do so may result in additional processing fees from our waste management provider. We believe that with everyone's cooperation, we can make our office a more sustainable workplace. Thank you for your attention to this important matter.",
    "question": "What is the focus of the memo?",
    "paraphrased_word": "internal message",
    "explanation": "「memo（社内連絡）」は「internal message」と言い換えられます。"
  },
  {
    "target_word": "Luggage",
    "theme": "航空会社の持ち込み制限",
    "passage": "Welcome to Pacific Airways. To ensure the comfort and safety of all passengers, please note our updated policy regarding carry-on baggage. Each traveler is permitted to bring one small suitcase and one personal item, such as a laptop bag or handbag, into the cabin. Items must fit under the seat in front of you or in the overhead compartment. Any oversized items will be checked at the gate for an additional fee. Please weigh your belongings at home to avoid delays at the airport. We also recommend labeling your possessions with your contact information. We wish you a pleasant flight and thank you for choosing our airline.",
    "question": "How many pieces of luggage are allowed in the cabin?",
    "paraphrased_word": "baggage",
    "explanation": "「luggage（手荷物）」の最も一般的な言い換えは「baggage」です。"
  },
  {
    "target_word": "Editor",
    "theme": "出版社の求人案内",
    "passage": "Are you passionate about literature and have a sharp eye for detail? Global Publishing is currently seeking a publications supervisor to join our fiction department. In this role, you will be responsible for reviewing manuscripts, coordinating with authors, and overseeing the final proofreading process before a book goes to print. The ideal candidate will have at least five years of experience in the publishing industry and excellent communication skills. We offer a competitive salary and a creative working environment in the heart of the city. If you are interested in shaping the next generation of best-sellers, please submit your resume and a cover letter by the end of the month.",
    "question": "What is a requirement for the new editor?",
    "paraphrased_word": "publications supervisor",
    "explanation": "「editor（編集者）」は、役割を説明する「publications supervisor（出版監督者）」という表現で言い換えられています。"
  },
  {
    "target_word": "Exhibition",
    "theme": "アートギャラリーの案内",
    "passage": "The Metropolitan Gallery is thrilled to present 'Nature's Silence,' an art show featuring the landscape paintings of Sarah Jenkins. This collection explores the beauty of the national parks through vibrant oil colors and unique textures. The display will be open to the public from March 1 to April 15 in the East Wing. Admission is free, but we suggest making a reservation online for weekend visits due to high demand. There will be a special opening reception on the first evening, where visitors can meet the artist and enjoy light refreshments. We look forward to sharing these stunning works of art with the local community.",
    "question": "When does the exhibition close?",
    "paraphrased_word": "art show",
    "explanation": "「exhibition（展示会）」は「art show（美術展）」と言い換えられます。"
  },
  {
    "target_word": "Leading",
    "theme": "企業紹介",
    "passage": "As a premier manufacturer of renewable energy components, Zenith Solar has been at the forefront of the industry for over two decades. We specialize in producing high-efficiency solar panels and battery storage systems for both residential and commercial use. Our products are distributed in over 30 countries, helping thousands of customers reduce their carbon footprint. Our commitment to innovation has earned us numerous awards for engineering excellence. Whether you are looking to upgrade your home or power a large factory, our team of experts is ready to provide you with the most reliable energy solutions on the market today. Contact us to learn more about our technology.",
    "question": "Why is Zenith Solar considered a leading company?",
    "paraphrased_word": "premier",
    "explanation": "「leading（一流の）」は「premier（最高の、第1位の）」と言い換えられます。"
  },
  {
    "target_word": "Organization",
    "theme": "チャリティー団体の活動",
    "passage": "The 'Clean Water Fund' is a non-profit association dedicated to providing safe drinking water to rural communities in developing nations. Since its founding in 2010, the group has successfully installed over 500 filtration systems and educated thousands of people on hygiene practices. We rely heavily on the generous donations of our supporters and the hard work of our volunteers to continue our mission. Every dollar contributed goes directly toward purchasing materials and funding local engineering projects. We believe that access to clean water is a basic human right. Join us in our efforts to make a lasting difference in the world by becoming a monthly donor today.",
    "question": "What is the primary goal of the organization?",
    "paraphrased_word": "association",
    "explanation": "「organization（組織、団体）」は「association（協会）」と言い換えられます。"
  },
  {
    "target_word": "Release",
    "theme": "新製品の発売",
    "passage": "TechNova is excited to announce the market launch of the NeoTab 5 this September. This new tablet features a revolutionary ultra-thin display and a battery that lasts up to 48 hours on a single charge. It also comes equipped with the latest processing chip, making it the fastest device in its category. Pre-orders will begin next Monday on our official website, and customers who order early will receive a complimentary protective case. We have been developing this technology for three years and are confident that it will set a new standard for mobile computing. Visit our showroom to experience the NeoTab 5 in person before the official date.",
    "question": "When is the product release scheduled?",
    "paraphrased_word": "market launch",
    "explanation": "「release（発売）」は、新製品の文脈では「market launch（市場投入）」と言い換えられます。"
  },
  {
    "target_word": "Limited",
    "theme": "期間限定のプロモーション",
    "passage": "For a restricted time only, City Fitness is offering a special enrollment deal for new members. If you join our gym before the end of this week, you will pay no registration fee and receive your first month of membership for free. This offer is only available at our downtown and uptown locations. Our facilities include state-of-the-art weight machines, a heated swimming pool, and a variety of group classes. Please note that this promotion is restricted to the first 100 people who sign up, so don't wait too long! Visit our front desk today to take advantage of this incredible opportunity to start your fitness journey at a great price.",
    "question": "Is the membership offer limited?",
    "paraphrased_word": "restricted",
    "explanation": "「limited（限られた）」は、条件の制限を示す「restricted」と言い換えられます。"
  },
  {
    "target_word": "Procedure",
    "theme": "入退室の手順",
    "passage": "All employees must follow the established steps for checking out equipment from the inventory room. First, you must log in to the digital tracking system using your employee ID. Second, select the items you need and record the serial numbers. Finally, ensure that a supervisor signs off on your request before you leave the premises. These guidelines are in place to ensure that all assets are accounted for and maintained properly. Equipment should be returned in the same condition it was borrowed within 24 hours. Failure to comply with these regulations may result in the loss of equipment borrowing privileges. Thank you for following our safety and security protocols.",
    "question": "What is the procedure for borrowing equipment?",
    "paraphrased_word": "established steps",
    "explanation": "「procedure（手順）」は「established steps（確立されたステップ）」と言い換えられます。"
  },
  {
    "target_word": "Experienced",
    "theme": "求人募集",
    "passage": "Apex Law Firm is looking for a seasoned professional to lead our international trade department. The successful applicant will have a deep understanding of maritime laws and at least ten years of practice in a senior role. We value candidates who have a proven track record of handling complex negotiations and providing strategic advice to high-profile clients. In return, we offer an attractive compensation package and a path to partnership within the firm. If you possess the necessary skills and a passion for legal excellence, please send your portfolio to our HR department. We look forward to reviewing your qualifications and potentially welcoming you to our team.",
    "question": "Why is the firm looking for an experienced lawyer?",
    "paraphrased_word": "seasoned",
    "explanation": "「experienced（経験豊富な）」は、熟練を表す「seasoned（熟練した）」と言い換えられます。"
  },
  {
    "target_word": "Personnel",
    "theme": "部署の問い合わせ先案内",
    "passage": "If you have any questions regarding your health insurance benefits or holiday allowance, please contact the staffing division on the third floor. Our team is available from 9:00 A.M. to 5:00 P.M. to assist you with any administrative concerns. Please remember to bring your employee ID card when you visit. For issues related to payroll or tax documents, you should contact the accounting department directly. We aim to provide all employees with the support they need to succeed in their roles. You can also find many resources and forms on the internal company portal under the 'Employee Services' section. We are here to help you manage your career at our company.",
    "question": "Which department should personnel contact for insurance questions?",
    "paraphrased_word": "staffing division",
    "explanation": "「personnel（職員・人事）」は「staffing division（人事部門）」と言い換えられます。"
  },
  {
    "target_word": "Author",
    "theme": "ブックイベントの告知",
    "passage": "The Downtown Library is excited to host a talk by the writer of the best-selling novel 'The Desert's Secret' next Tuesday at 6:30 P.M. During this session, the guest will discuss the inspiration behind the story and the challenges of writing historical fiction. Following the presentation, there will be a book signing and a brief question-and-answer period. Copies of the book will be available for purchase at a discounted price during the event. This is a rare opportunity to meet a famous creator and learn about the creative process firsthand. Seating is available on a first-come, first-served basis, so we recommend arriving early to ensure you get a good spot.",
    "question": "Who will be the guest author at the library event?",
    "paraphrased_word": "writer",
    "explanation": "「author（著者）」の最も分かりやすい言い換えは「writer（作家・書き手）」です。"
  },
  {
    "target_word": "Benefit",
    "theme": "新制度のメリット",
    "passage": "Our new transit subsidy program offers several advantages for employees who commute using public transportation. One major perk is that the company will cover up to 50% of your monthly train or bus pass. This initiative not only helps you save money but also encourages more sustainable travel habits. To apply for the subsidy, simply submit a copy of your monthly receipt to the finance department through the online portal. We believe that this support will make the daily commute more manageable and affordable for everyone. We are committed to improving the work-life quality of our staff and will continue to explore other ways to provide valuable support to our team.",
    "question": "What is one benefit of the transit subsidy program?",
    "paraphrased_word": "perk",
    "explanation": "「benefit（恩恵、手当）」は、特典やメリットを指す「perk」と言い換えられます。"
  },
  {
    "target_word": "Focus",
    "theme": "会議の議題設定",
    "passage": "At our next strategy meeting, we will emphasize digital marketing and social media engagement to reach a younger audience. Our previous campaigns relied heavily on television and print media, but the latest data shows that our target customers spend most of their time online. Therefore, we plan to shift our resources toward creating viral video content and partnering with popular influencers. We will also analyze the performance of our current website and discuss potential improvements to the user interface. Please come prepared with your creative ideas and any successful case studies from other companies. Our goal is to stay competitive in an increasingly digital world.",
    "question": "What will the marketing team focus on at the meeting?",
    "paraphrased_word": "emphasize",
    "explanation": "「focus on（〜に重点を置く）」は「emphasize（〜を強調する）」に言い換えられます。"
  },
  {
    "target_word": "Participate",
    "theme": "地域清掃活動への参加呼びかけ",
    "passage": "Dear Employees, our annual Community Cleanup Day is scheduled for next Saturday. We invite all staff members to take part in this rewarding event as we work together to beautify the park adjacent to our headquarters. Gloves and trash bags will be provided, and a complimentary lunch will be served at noon for all volunteers. Please sign up on the company intranet by Wednesday afternoon so we can finalize the catering arrangements. This is a great opportunity to give back to the neighborhood and build stronger bonds with your colleagues. We hope to see a large turnout this year. Thank you for your continued support and dedication to our community initiatives.",
    "question": "Who is invited to participate in the cleanup event?",
    "paraphrased_word": "take part in",
    "explanation": "「participate（参加する）」の言い換えとして「take part in」は非常に頻出します。"
  },
  {
    "target_word": "Cause",
    "theme": "悪天候による配送遅延の通知",
    "passage": "To our valued customers, please be advised that a severe winter storm is currently affecting several regions across the country. These extreme weather conditions will likely result in temporary delays for all ground shipments scheduled for this week. Our logistics team is monitoring the situation closely and working hard to minimize the impact on our delivery schedule. We recommend checking your tracking number on our website for the most up-to-date information regarding your package. We apologize for any inconvenience this may lead to and appreciate your patience as we prioritize the safety of our drivers and staff during this time. Thank you for choosing our service.",
    "question": "What will cause the delivery delays this week?",
    "paraphrased_word": "result in",
    "explanation": "原因から結果を導く表現として、「cause（引き起こす）」は「result in」という構造で言い換えられます。"
  },
  {
    "target_word": "Degree",
    "theme": "会計士の求人募集",
    "passage": "Bright Finance is currently seeking a motivated Junior Accountant to join our expanding team. The ideal candidate will be responsible for managing payroll, preparing monthly financial reports, and assisting with tax filings. Applicants must possess a university qualification in accounting or a related field. Additionally, at least two years of experience in a professional office environment is highly preferred. We offer a competitive salary, comprehensive health benefits, and excellent opportunities for career advancement. If you are a detail-oriented individual with strong analytical skills, please submit your resume and a cover letter through our online recruitment portal by the end of the month. We look forward to hearing from you.",
    "question": "Is a university degree required for the position?",
    "paraphrased_word": "qualification",
    "explanation": "「degree（学位）」は、学歴や資格を示す「qualification」と言い換えられます。"
  },
  {
    "target_word": "Directly",
    "theme": "新しい問い合わせ窓口の案内",
    "passage": "Attention all clients: To better serve your needs, we have updated our customer support system. Starting Monday, if you have any questions regarding your billing statement or account status, you can speak straight to a representative by calling our new toll-free hotline. This change aims to reduce waiting times and provide more personalized assistance. Previously, all inquiries were handled through an automated email system, which often caused delays in response. Please note that our office hours remain the same, from 9:00 A.M. to 6:00 P.M., Monday through Friday. We appreciate your continued business and look forward to providing you with more efficient service under our new system.",
    "question": "How can customers contact a representative directly?",
    "paraphrased_word": "straight",
    "explanation": "「directly（直接）」は、ダイレクトにやり取りをすることを表す「straight」と言い換えられます。"
  },
  {
    "target_word": "Host",
    "theme": "技術セミナーの開催告知",
    "passage": "The International Tech Association is excited to organize a series of workshops on artificial intelligence this coming November. These sessions will be held at the Metropolitan Convention Center and will feature keynote speeches from industry leaders and hands-on training for developers. The goal of this event is to foster innovation and provide a platform for networking among technology professionals. Tickets are available for purchase on our website, and we offer a discounted rate for students and small business owners. Don't miss this opportunity to learn about the latest trends and connect with experts in the field. We look forward to welcoming you to this landmark event in our city.",
    "question": "Who will host the technology workshops in November?",
    "paraphrased_word": "organize",
    "explanation": "イベントを主催することを指す「host」は、計画・準備を統括する「organize（企画する）」と言い換えられます。"
  },
  {
    "target_word": "Expert",
    "theme": "コンサルティングサービスの宣伝",
    "passage": "Are you looking to optimize your company's supply chain? At Global Logistics Solutions, we provide personalized consulting services to help businesses reduce costs and improve efficiency. Our team of specialists has over 20 years of experience in international trade and transportation. We analyze your current operations and provide actionable recommendations tailored to your specific goals. Whether you are a small startup or a large corporation, we have the knowledge and tools to help you succeed in a competitive market. Contact us today to schedule a free initial consultation and find out how we can support your growth. Your success is our priority, and we are committed to delivering measurable results.",
    "question": "Why should a company hire an expert from this firm?",
    "paraphrased_word": "specialists",
    "explanation": "「expert（専門家）」の言い換えとして、特定の分野に精通した「specialist」が使われています。"
  },
  {
    "target_word": "Impress",
    "theme": "採用面接後の内部評価メモ",
    "passage": "To: Hiring Committee\nFrom: Sarah Miller, Marketing Director\nSubject: Interview Feedback - James Chen\n\nI met with James Chen yesterday for the Senior Designer position. Overall, his portfolio was quite strong, and his creative vision stood out to me during our discussion. He clearly explained his process for developing brand identities and showed several successful case studies from his previous role. His technical skills are exactly what we are looking for to lead our upcoming digital campaign. While he has slightly less experience with video editing than we initially requested, his enthusiasm and problem-solving abilities more than make up for it. I recommend moving him to the final round of interviews with the executive team next week.",
    "question": "How did James Chen impress the Marketing Director?",
    "paraphrased_word": "stood out to",
    "explanation": "「impress（好印象を与える）」は、「stand out to（〜の目を引く、際立つ）」という表現に連動します。"
  },
  {
    "target_word": "Mainly",
    "theme": "企業の事業拡大に関するプレスリリース",
    "passage": "Green Energy Corp is pleased to announce the opening of its new research facility in Berlin. This expansion is primarily focused on developing advanced battery technologies for electric vehicles. By investing in this new site, the company aims to accelerate its innovation cycle and maintain a competitive edge in the European market. The facility will employ over 100 researchers and engineers from around the world. In addition to battery research, the center will also explore sustainable materials for solar panels. This move represents a significant milestone in our commitment to a carbon-neutral future. We are excited about the potential collaborations this new location will foster within the local tech community.",
    "question": "What is the new facility mainly used for?",
    "paraphrased_word": "primarily",
    "explanation": "「mainly（主に）」は、TOEICにおいて重要語である「primarily（主として）」と言い換えられるケースが非常に多いです。"
  },
  {
    "target_word": "Suggestion",
    "theme": "従業員アンケートへの回答",
    "passage": "Thank you to everyone who participated in last month's office environment survey. We received many valuable insights regarding our current workspace. One common recommendation was to increase the number of private meeting rooms to facilitate focused collaboration. In response, the management team has decided to renovate the third-floor lounge into three small conference pods by the end of the year. We are also looking into upgrading the kitchen facilities based on your feedback about the coffee machines. We appreciate your input and are committed to making our office a more comfortable and productive place for everyone. Please continue to share your ideas with the HR department.",
    "question": "What was a common suggestion from the employees?",
    "paraphrased_word": "recommendation",
    "explanation": "アンケートにおける「suggestion（提案）」は、改善を推奨する「recommendation（推奨）」と言い換えられます。"
  },
  {
    "target_word": "Supplier",
    "theme": "原材料の在庫不足に関するメモ",
    "passage": "To: Production Team\nFrom: Mark Davis, Purchasing Manager\n\nPlease be informed that we are currently experiencing a shortage of high-grade aluminum. Our primary vendor has notified us that a strike at their processing plant has caused a temporary halt in shipments. As a result, we may need to adjust our production schedule for the next two weeks. We are currently contacting alternative sources to secure the necessary materials, but prices are expected to be slightly higher. Please prioritize the completion of existing orders for our premium clients. We will provide another update as soon as we have a confirmed delivery date for the new shipment. Thank you for your flexibility and cooperation during this challenging period.",
    "question": "Which supplier is unable to deliver materials?",
    "paraphrased_word": "vendor",
    "explanation": "「supplier（供給業者）」の最も代表的な言い換えは「vendor（販売業者）」です。"
  },
  {
    "target_word": "Document",
    "theme": "契約書の確認依頼メール",
    "passage": "Dear Mr. Thompson, I have attached the final version of the service agreement for your review. Please examine the paperwork carefully to ensure that all the terms we discussed, including the project timeline and payment schedule, are accurately reflected. If everything is in order, please sign the last page and return a scanned copy to me by Friday afternoon. If you require any further adjustments to the clauses regarding intellectual property, let know as soon as possible so we can consult our legal department. Once we receive the signed copy, we will begin the onboarding process for your team. We look forward to a successful partnership with your company.",
    "question": "What should Mr. Thompson do after reviewing the document?",
    "paraphrased_word": "paperwork",
    "explanation": "「document（書類）」は、包括して指す「paperwork（書類、提出書類）」と言い換えられることがあります。"
  },
  {
    "target_word": "Remind",
    "theme": "安全講習の受講期限の通知",
    "passage": "To all staff: This is to point out that the deadline for completing the mandatory annual safety training is this Friday, June 10. According to our records, several employees have not yet started the online modules. Please remember that completion of this course is a requirement for all personnel to ensure a safe working environment and compliance with city regulations. The training takes approximately one hour and can be accessed through the employee portal under the 'Compliance' tab. If you encounter any technical issues, please contact the IT help desk immediately. Thank you for your prompt attention to this matter and for your commitment to workplace safety.",
    "question": "Why did the manager remind the staff?",
    "paraphrased_word": "point out",
    "explanation": "「remind（気付かせる、思い出させる）」という行為は、本文の「point out（指摘する）」と連動しています。"
  },
  {
    "target_word": "Require",
    "theme": "社内イベントのドレスコード規定",
    "passage": "Dear Colleagues, we are looking forward to our annual awards banquet this Friday evening at the Grand Hotel. We would like to clarify that formal attire is mandatory for this event. Men are expected to wear a suit and tie, while women should wear a formal dress or a professional suit. This choice reflects the significance of the achievements we are celebrating and the elegant nature of the venue. Please arrive at the ballroom by 7:00 P.M. for the welcome reception. Dinner will be served at 8:00 P.M., followed by the presentation of awards. We appreciate your cooperation in making this a truly special and professional evening for everyone involved.",
    "question": "What does the policy require for the banquet?",
    "paraphrased_word": "mandatory",
    "explanation": "「require（要求する）」という内容は、本文中で「mandatory（必須の）」という形容詞を使って根拠付けられます。"
  },
  {
    "target_word": "Representative",
    "theme": "カスタマーサービスの連絡先案内",
    "passage": "Thank you for purchasing a HomeTech smart thermostat. If you experience any difficulties during the installation process, our technical support team is here to help. You can connect with a service agent by using the live chat feature on our website or by calling our support line at 1-800-555-0199. Our staff is available 24/7 to provide troubleshooting tips and step-by-step guidance. For less urgent inquiries, you can also browse our online help center, which contains video tutorials and a list of frequently asked questions. We are dedicated to ensuring you get the most out of our products and appreciate your business. Welcome to the HomeTech family!",
    "question": "How can a customer speak with a representative?",
    "paraphrased_word": "agent",
    "explanation": "「representative（担当者）」は、顧客対応の文脈において「agent（担当スタッフ）」と言い換えられます。"
  },
  {
    "target_word": "Packaging",
    "theme": "新製品の環境配慮型デザイン",
    "passage": "EcoBeauty is proud to announce the launch of its new organic skincare line. In our continued effort to protect the planet, we have redesigned our product wrapping to be 100% plastic-free. Our new bottles are made from recycled glass, and the outer boxes are constructed from biodegradable cardboard printed with soy-based inks. We believe that beauty products should not come at the expense of the environment. These changes will help us reduce our carbon footprint by an estimated 20% over the next year. You can find our new eco-friendly collection at all major retailers starting next month. Join us in our mission to create a cleaner, greener future for everyone.",
    "question": "What is special about the new packaging?",
    "paraphrased_word": "wrapping",
    "explanation": "「packaging（包装）」は、商品を包み込む外装材を指す「wrapping」に言い換えられます。"
  },
  {
    "target_word": "Description",
    "theme": "不動産物件の紹介",
    "passage": "Modern Living Real Estate is pleased to offer this stunning two-bedroom apartment located in the heart of the financial district. For a full list of features and property details, please visit our website and enter reference number #5521. This unit features floor-to-ceiling windows, a private balcony with city views, and high-end stainless steel appliances. The building also offers a 24-hour gym, a rooftop swimming pool, and secure underground parking. It is ideally situated within walking distance of major subway lines and popular restaurants. To schedule a viewing or to request more information, please contact our office during business hours. This property is expected to be taken quickly, so don't delay!",
    "question": "Where can the full description of the apartment be found?",
    "paraphrased_word": "details",
    "explanation": "細かく記した「description（説明）」は、詳細項目を意味する「details（詳細情報）」と言い換えられます。"
  },
  {
    "target_word": "Property",
    "theme": "オフィススペースの賃貸案内",
    "passage": "This prime real estate is now available for lease in the growing tech hub of North Riverside. The building offers over 10,000 square feet of flexible office space, including open-plan areas and private executive suites. It is equipped with fiber-optic internet and a modern security system. Located near the central train station, the site provides easy access for commuters and clients alike. Plenty of parking is available for both staff and visitors. The landlord is offering a six-month rent discount for tenants who sign a three-year lease before the end of the quarter. For more information or to arrange a tour of the premises, please contact our leasing agent today.",
    "question": "What kind of property is being offered for lease?",
    "paraphrased_word": "real estate",
    "explanation": "「property（不動産）」は、賃貸の広告内では「real estate（不動産）」と直接言い換えられます。"
  },
  {
    "target_word": "Extension",
    "theme": "プロジェクトの期限延長の承認",
    "passage": "Dear Project Team, I have reviewed your request for more time to complete the final phase of the website redesign. Given the technical challenges with the database integration that occurred last week, I have decided to grant a ten-day extra time for the project. The new deadline for the final launch will be Friday, October 20. Please use this additional time to ensure that all security protocols are thoroughly tested and that the user interface is fully optimized for mobile devices. I will be checking in with the team on Wednesday to review your progress. Thank you for your hard work and dedication to making this project a success despite the unexpected setbacks.",
    "question": "Why was the extension granted for the project?",
    "paraphrased_word": "extra time",
    "explanation": "スケジュールの「extension（延長）」は、意味の「extra time（追加の時間）」に言い換えられます。"
  },
  {
    "target_word": "Inquire",
    "theme": "製品の在庫確認メール",
    "passage": "Dear Sales Team, I am writing to ask about the availability of the Model X100 printer in your downtown showroom. I noticed on your website that this model is currently listed as 'limited stock,' and I wanted to know if you have at least three units ready for immediate purchase. If they are available, could you also provide a quote for professional installation and a three-year extended warranty? I am planning to visit the store this Thursday morning and would appreciate a quick response so I can finalize my budget. If the X100 is not in stock, please let me know if there are any comparable models that you would recommend for a small office. Thank you.",
    "question": "What did the customer inquire about in the email?",
    "paraphrased_word": "ask about",
    "explanation": "「inquire（問い合わせる）」という動詞は、おなじみの表現である「ask about」に言い換えられます。"
  },
  {
    "target_word": "Merchandise",
    "theme": "季節外れ商品のクリアランスセール",
    "passage": "Summer is coming to an end, and it's time for our massive seasonal clearance! Starting this Friday, 'Urban Fashion' will be offering discounts of up to 70% on all remaining summer goods. This includes our entire collection of swimwear, shorts, and light linen shirts. We need to make room for our new autumn arrivals, so everything must go! Please note that all sales during this period are final and cannot be returned or exchanged. Visit our store early to get the best selection of sizes and styles. Our doors open at 9:00 A.M., and we will have extra staff on hand to assist you with your purchases. Don't miss out on these incredible savings!",
    "question": "Which merchandise is discounted up to 70%?",
    "paraphrased_word": "goods",
    "explanation": "「merchandise（商品）」は、品物を表す「goods（商品類）」に頻繁に言い換えられます。"
  },
  {
    "target_word": "Highly",
    "theme": "新製品のレビュー",
    "passage": "I am writing to share my feedback on the X-2000 office chair I purchased last month. As a freelance designer who spends over ten hours a day at a desk, comfort is essential for me. I found the ergonomic support of this model to be extremely impressive. The adjustable armrests and lumbar support have significantly reduced my back pain. Although the price is a bit higher than other brands, the build quality justifies the cost. I would certainly recommend this product to anyone looking for a durable workspace solution. It has made a noticeable difference in my daily productivity and overall well-being.",
    "question": "What does the writer think is highly impressive about the chair?",
    "paraphrased_word": "extremely",
    "explanation": "強調する副詞としての「highly（非常に）」は、「extremely（極めて）」と言い換えられます。"
  },
  {
    "target_word": "Result",
    "theme": "プロジェクトの業績報告",
    "passage": "Dear Team, I am pleased to share the success of our recent summer marketing campaign. Due to our increased presence on social media and the new partnership with local influencers, we saw a 25% rise in website traffic. This positive outcome has led to a record-breaking number of new subscriptions this month. Our analysis suggests that the video demonstrations were particularly effective in engaging younger audiences. I want to thank everyone for their hard work and creativity. We will hold a brief meeting on Friday to discuss how we can maintain this momentum as we move into the next phase of our growth strategy.",
    "question": "What was the result of the summer marketing campaign?",
    "paraphrased_word": "outcome",
    "explanation": "活動がもたらした「result（結果）」は、数値を表す「outcome（成果）」に言い換えられます。"
  },
  {
    "target_word": "Assistance",
    "theme": "ITサポートへの問い合わせ",
    "passage": "To: All Staff\nFrom: IT Department\nSubject: Software Migration\n\nPlease be advised that we will be migrating all employee accounts to the new cloud system this weekend. The process will begin at 6:00 P.M. on Friday and is expected to be completed by Sunday morning. If you require any help with accessing your files or setting up your new password on Monday, our technicians will be available in the main lobby. We have also uploaded a series of video tutorials to the internal portal. Please review these materials before contacting the help desk. We appreciate your patience as we upgrade our infrastructure to serve you better.",
    "question": "Where can employees get assistance on Monday morning?",
    "paraphrased_word": "help",
    "explanation": "「assistance（援助）」の最も一般的な言い換え表現は、シンプルな「help」です。"
  },
  {
    "target_word": "Encourage",
    "theme": "社内ワークショップの案内",
    "passage": "We are excited to announce a series of professional development workshops starting next month. These sessions will cover various topics, including advanced Excel techniques and effective public speaking. We strongly urge all team members to take advantage of these learning opportunities to enhance their skill sets. Participation is voluntary, but those who attend at least three sessions will receive a certificate of completion. Please sign up through the HR portal by the end of this week to secure your spot. We believe that continuous learning is the key to our collective success and look forward to seeing many of you there.",
    "question": "What does the company encourage its employees to do?",
    "paraphrased_word": "urge",
    "explanation": "「encourage（促す）」は、強くプッシュする動詞「urge（強く促す）」にリンクすることが多いです。"
  },
  {
    "target_word": "Individual",
    "theme": "トレーニングセッションの準備",
    "passage": "The mandatory safety training session will take place in the conference hall this Wednesday at 10:00 A.M. To ensure the session runs smoothly and remains interactive, the number of participants is limited to 20. Each person is required to bring a laptop and a pair of headphones for the practical exercises. Please make sure your devices are fully charged, as power outlets in the hall are limited. If you cannot attend this session, please notify your supervisor by Tuesday morning so we can reschedule. Documentation of your attendance is necessary for our annual compliance audit. Thank you for your cooperation.",
    "question": "What must each individual bring to the training session?",
    "paraphrased_word": "Each person",
    "explanation": "「individual（個人）」は、本文で「Each person（各人）」と言い換えられます。"
  },
  {
    "target_word": "Laboratory",
    "theme": "新製品開発の進捗",
    "passage": "The development of our new eco-friendly cleaning solution is reaching its final stages. Our team at the main research facility has been testing the formula for the past six months to ensure it meets international safety standards. Initial results show that the product is 95% biodegradable while maintaining high cleaning performance. We are now preparing for small-scale production trials next month. If these tests are successful, we hope to launch the product in early spring. We would like to thank our dedicated scientists for their commitment to innovation. A full technical report will be shared at the next board meeting.",
    "question": "Where is the product currently being tested in the laboratory?",
    "paraphrased_word": "research facility",
    "explanation": "「laboratory（実験室）」は、開発拠点を指す「research facility」と言い換えられます。"
  },
  {
    "target_word": "Consider",
    "theme": "採用面接後の連絡",
    "passage": "Dear Mr. Henderson, thank you for visiting our office yesterday to interview for the Marketing Manager position. Our team enjoyed learning about your extensive experience in digital advertising and brand strategy. We are currently interviewing several other candidates and expect to make a final decision by next Friday. In the meantime, please take a moment to think about the salary expectations and benefits package we discussed. If you have any further questions or would like to provide additional references, please feel free to email us. We appreciate your interest in joining Global Solutions and will be in touch with you shortly regarding the next steps.",
    "question": "What is Mr. Henderson asked to consider?",
    "paraphrased_word": "think about",
    "explanation": "「consider（検討する）」という思考動詞は、熟語表現の「think about」に言い換えられます。"
  },
  {
    "target_word": "Headquarters",
    "theme": "役員会議の場所案内",
    "passage": "To all regional managers, this is a reminder that the annual strategy summit will take place next month. This year, the event will be held at our main office in Seattle to allow participants to tour our newly expanded distribution center. The summit will cover our goals for the upcoming fiscal year and include workshops on leadership and market expansion. Please ensure you have booked your flights and accommodation by the end of this week. Travel expenses will be reimbursed according to the company policy. We look forward to a productive week of collaboration and planning with all our leaders from across the country.",
    "question": "Where is the company's headquarters located?",
    "paraphrased_word": "main office",
    "explanation": "「headquarters（本社）」の最も定番の言い換えは「main office」です。"
  },
  {
    "target_word": "Ship",
    "theme": "注文の発送状況",
    "passage": "Dear Customer, thank you for your recent purchase from TechGear Online. We are pleased to inform you that your order #88412 is ready for delivery. Our warehouse team will dispatch the items via express courier tomorrow morning. You will receive another notification containing a tracking number once the package has left our facility. Please note that a signature will be required upon arrival. If you are not available to receive the package, the courier will leave a notice with instructions for rescheduling. We hope you enjoy your new equipment and thank you for choosing TechGear for your electronic needs.",
    "question": "When will the company ship the order?",
    "paraphrased_word": "dispatch",
    "explanation": "「ship（発送する）」は、物流用語の「dispatch（発送する）」と言い換えられます。"
  },
  {
    "target_word": "Commercial",
    "theme": "新しいテレビ広告の撮影",
    "passage": "Attention Employees: We are excited to announce that a professional film crew will be on-site this Thursday. They will be filming a new television advertisement for our latest line of home appliances. As a result, the main lobby and the second-floor cafeteria will be closed to staff between 9:00 A.M. and 2:00 P.M. Please use the side entrance and the breakroom on the third floor during this time. We apologize for any inconvenience this may cause and appreciate your cooperation. This new marketing campaign is an important step in increasing our brand awareness nationwide, and we are proud to showcase our modern office environment.",
    "question": "What is the purpose of filming the commercial?",
    "paraphrased_word": "advertisement",
    "explanation": "「commercial（コマーシャル広告）」は、広く「advertisement（広告）」と言い換えられます。"
  },
  {
    "target_word": "Device",
    "theme": "オフィスの設備トラブル",
    "passage": "To: All Staff\nFrom: Facilities Management\n\nWe have been notified that the multi-function printer on the fourth floor is currently out of order. A technician has been called and is expected to arrive this afternoon to repair the machine. In the meantime, please use the printers located in the East Wing or the basement. We apologize for the frustration this may cause, especially during this busy reporting period. Please do not attempt to fix the equipment yourself, as this may void the warranty. We will send another update once the repairs are complete and the service is restored. Thank you for your patience and understanding.",
    "question": "What is wrong with the device on the fourth floor?",
    "paraphrased_word": "machine",
    "explanation": "「device（装置）」は、事務機器であれば「machine（機械）」と言い換えられます。"
  },
  {
    "target_word": "Intended",
    "theme": "新サービスのターゲット層",
    "passage": "The 'Freelance Pro' software suite is now available for download. This comprehensive set of tools was specifically designed for independent contractors and small business owners who need to manage their finances and project timelines efficiently. It features automated invoicing, time-tracking, and expense reporting in one easy-to-use interface. To celebrate the launch, we are offering a 30-day free trial for all new users. We believe that these features will save you hours of administrative work each week, allowing you to focus on your creative projects. Visit our website to see a full list of specifications and system requirements.",
    "question": "Who is the software mainly intended for?",
    "paraphrased_word": "designed for",
    "explanation": "「intended for（〜向けである）」は、「designed for」と言い換えられます。"
  },
  {
    "target_word": "Brochure",
    "theme": "観光ツアーの案内",
    "passage": "Discover the hidden gems of the Mediterranean with Ocean View Cruises! Our upcoming winter tours offer a perfect blend of history, culture, and relaxation. For more detailed information on our itineraries and cabin options, please refer to the enclosed pamphlet. You can also view videos of our previous trips on our official social media pages. Early-bird bookings made before the end of this month will receive a $200 discount per person. Our luxury ships feature world-class dining, live entertainment, and guided excursions at every port. Don't miss this opportunity to create unforgettable memories. Contact our travel experts today to book your dream vacation.",
    "question": "Where can customers find more details about the tour in the brochure?",
    "paraphrased_word": "pamphlet",
    "explanation": "小冊子広告を意味する「brochure」の最も代表的な言い換えは「pamphlet（パンフレット）」です。"
  },
  {
    "target_word": "Mail",
    "theme": "更新通知の送付方法",
    "passage": "Dear Subscriber, your annual membership with the City Library is set to expire on November 30. To ensure uninterrupted access to our digital collection and physical books, please renew your account before that date. A formal renewal notice was sent to your home address by post last Friday, containing your unique membership ID and instructions for online payment. You can also renew in person at any of our branches. Members who renew before the expiration date will receive a complimentary tote bag. If you have already processed your renewal, please disregard this message. Thank you for being a part of our community and for supporting our local library.",
    "question": "How was the renewal notice sent via mail?",
    "paraphrased_word": "post",
    "explanation": "郵便配送手段としての「mail」は、「post（郵便）」と言い換えられます。"
  },
  {
    "target_word": "Prefer",
    "theme": "オフィスのレイアウト調査",
    "passage": "Thank you for participating in the workplace environment survey conducted last month. The results indicate that a majority of staff members would rather work in a quiet, private area than in an open-plan office. In response to this feedback, we have decided to install soundproof partitions and create more dedicated quiet zones on each floor. These changes are scheduled to begin next weekend and will be completed within two weeks. We hope these improvements will help you focus better and improve your overall job satisfaction. We appreciate your honest input and will continue to look for ways to make our office a better place to work.",
    "question": "What kind of workspace do the majority of staff members prefer?",
    "paraphrased_word": "would rather",
    "explanation": "「prefer（〜を好む）」という動詞は、「would rather（むしろ〜したい）」と言い換えられます。"
  },
  {
    "target_word": "Response",
    "theme": "顧客からの問い合わせへの返信",
    "passage": "Dear Ms. Green, thank you for your inquiry regarding our bulk pricing for office furniture. In reply to your email, I have attached a detailed price list for our most popular desks and chairs. For orders exceeding 50 units, we can offer a 15% discount on the total cost. Furthermore, we provide free assembly and delivery for all corporate clients within the metropolitan area. If you would like to schedule a visit to our showroom to see the items in person, please let me know. I would be happy to arrange a guided tour and answer any further questions you may have. We look forward to the possibility of working with your company.",
    "question": "What did the sender include in the response?",
    "paraphrased_word": "reply",
    "explanation": "「response（返答）」の名詞としての直接的な言い換え表現は「reply（返事）」です。"
  },
  {
    "target_word": "Region",
    "theme": "事業拡大のニュース",
    "passage": "Global Logistics is proud to announce its expansion into the Southeast Asian market. We will be opening three new distribution centers in this territory over the next twelve months to meet the growing demand for our shipping services. This move is expected to create over 200 new jobs for local workers and strengthen our delivery network in the area. Our CEO, Mr. Robert Vance, stated that this expansion is a key part of our five-year plan to become the leading logistics provider in the world. We are currently recruiting managers for these new sites. For more information on career opportunities, please visit the 'Global Expansion' tab on our website.",
    "question": "In which region is the company opening new distribution centers?",
    "paraphrased_word": "territory",
    "explanation": "地理的な区域を特定する「region（地域）」は、「territory（領土、地域）」と言い換えられます。"
  },
  {
    "target_word": "Donation",
    "theme": "チャリティーイベントの報告",
    "passage": "The local animal shelter would like to express its sincere gratitude for the successful fundraising event held last Saturday. Thanks to the generosity of our community, we raised over $5,000 to help provide food and medical care for the animals. Every contribution makes a significant difference in our ability to rescue and care for abandoned pets. We would also like to thank the volunteers who spent their weekend assisting with the event organization and the local businesses that provided items for the auction. We are a non-profit organization and rely entirely on the support of people like you. Thank you for helping us give these animals a second chance at a happy life.",
    "question": "What is the purpose of the donation to the shelter?",
    "paraphrased_word": "contribution",
    "explanation": "資金集めの文脈における「donation（寄付）」は、「contribution（寄付、貢献）」にリンクします。"
  },
  {
    "target_word": "Quarter",
    "theme": "収支報告の案内",
    "passage": "To: All Department Heads\nFrom: Finance Director\nSubject: Financial Review Meeting\n\nPlease be prepared to discuss your department's performance during the last three-month period at our meeting on Thursday. We will be reviewing our revenue targets, expense reports, and budget allocations for the next term. Each manager is expected to provide a brief presentation on their team's achievements and any challenges faced. Please submit your digital reports to the accounting department by Wednesday evening so they can be compiled into the main presentation. This review is crucial for ensuring we stay on track to meet our end-of-year financial goals. The meeting will be held in Conference Room A at 2:00 P.M.",
    "question": "What will be discussed regarding the last quarter?",
    "paraphrased_word": "three-month period",
    "explanation": "「quarter（四半期）」という期間は、「three-month period（3ヶ月の期間）」と言い換えられます。"
  },
  {
    "target_word": "Agreement",
    "theme": "契約の最終確認",
    "passage": "Dear Ms. Sterling, I have attached the final version of the lease contract for the office space on Miller Road. Please review the terms and conditions carefully, especially the sections regarding the maintenance responsibilities and the duration of the lease. If you find everything to be in order, please sign the document and return it to our office by the end of the week. Once we receive the signed copy, we will finalize the paperwork and hand over the keys next Monday. We are very pleased to have you as a tenant in our building and look forward to a long and successful relationship. If you have any questions, please contact our legal representative.",
    "question": "What is Ms. Sterling asked to do with the agreement?",
    "paraphrased_word": "contract",
    "explanation": "「agreement（契約、合意文書）」は、「contract（契約書）」と言い換えられます。"
  },
  {
    "target_word": "Journal",
    "theme": "学術雑誌への投稿案内",
    "passage": "Dear Dr. Miller, thank you for your interest in submitting your research to 'Global Science Weekly.' Our publication focuses on the latest advancements in biotechnology and environmental science. Before you upload your manuscript, please ensure that it follows our formatting guidelines, which can be found on our website. All submissions are reviewed by a panel of experts in the field. If your paper is selected, it will be featured in an upcoming issue later this year. We receive hundreds of articles each month, so it may take up to six weeks for our team to provide initial feedback. We appreciate your patience and look forward to reviewing your work.",
    "question": "What is the main topic of the journal mentioned in the email?",
    "paraphrased_word": "publication",
    "explanation": "定期刊行物や専門誌を指す「journal」は、「publication（出版物）」と言い換えられます。"
  },
  {
    "target_word": "Distribute",
    "theme": "社内資料の配布",
    "passage": "Attention all project managers: We will be holding a strategy meeting in Conference Room B tomorrow at 10:00 A.M. to discuss the Q3 budget. Please bring your laptops to access the digital presentation. During the session, we will hand out printed copies of the revised project timeline and the new expense policy. It is essential that everyone reviews these documents before the end of the week. If you are unable to go to the meeting in person, a recorded version will be available on the company server by Friday. Please notify your supervisor as soon as possible if you have any scheduling conflicts. Thank you for your cooperation.",
    "question": "What will the managers distribute during the meeting?",
    "paraphrased_word": "hand out",
    "explanation": "「distribute（配布する）」という動作の句動詞表現は「hand out」です。"
  },
  {
    "target_word": "Potential",
    "theme": "新規顧客の獲得戦略",
    "passage": "To: Sales Department\nFrom: Robert Chen, Sales Director\nSubject: New Market Expansion\n\nAs we look to expand our business into Northern Europe, our primary goal for this quarter is to identify prospective clients in the renewable energy sector. We have already started analyzing market trends and gathering contact information for major companies in the region. We will host a webinar next Tuesday to introduce our latest solar panel technology. Please prepare a list of leads and send out email invitations by the end of this week. We believe that this region offers a significant opportunity for growth, and your efforts in reaching out to new business partners are crucial to our success.",
    "question": "Who is the sales department trying to find for potential business?",
    "paraphrased_word": "prospective",
    "explanation": "「potential（潜在的な、見込みのある）」は、将来の顧客を指す際に「prospective（見込みのある）」と言い換えられます。"
  },
  {
    "target_word": "Reschedule",
    "theme": "会議の日程変更",
    "passage": "Dear Team, I am writing to inform you that we need to move our weekly progress meeting to a later time. Due to an urgent client call that several managers must attend, the session originally planned for 9:00 A.M. tomorrow will now take place at 3:00 P.M. on the same day. The meeting room will remain the same. I apologize for any inconvenience this last-minute adjustment may cause to your daily schedule. If you have a conflict with the new time, please let me know by this evening so we can arrange a separate briefing. Please remember to bring the updated project reports we discussed yesterday. Thank you for your flexibility.",
    "question": "Why did the manager need to reschedule the meeting?",
    "paraphrased_word": "move",
    "explanation": "「reschedule（予定を変更する）」は、具体的に日時をずらす意味で「move」と言い換えられます。"
  },
  {
    "target_word": "Renew",
    "theme": "契約の更新",
    "passage": "Dear Mr. Thompson, your current software subscription for 'ProDesign 5' is set to expire in 30 days. To ensure uninterrupted access to our cloud-based tools and technical support, we recommend that you extend your membership before the expiration date. You can do this easily by logging into your account on our website and selecting the 'Annual Plan' option. If you choose to do so before the end of this week, you will receive a 15% discount on the total cost. Please note that after the expiration date, your account will be downgraded to the basic free version, and you will lose access to premium features. Thank you for your continued business with us.",
    "question": "What is the customer encouraged to renew?",
    "paraphrased_word": "extend",
    "explanation": "期間を延ばすという意味の「renew（更新する）」は、「extend（延長する、更新する）」と言い換えられます。"
  },
  {
    "target_word": "Warehouse",
    "theme": "在庫管理施設の移転",
    "passage": "Due to our rapid growth over the past two years, we are excited to announce that we are moving our main storage facility to a larger location in the industrial park. The new site offers double the floor space and features advanced climate control systems to better protect our sensitive electronics. This transition will take place over the next two weekends to minimize disruption to our shipping schedule. During this time, please be aware that there may be slight delays in processing domestic orders. Our customer service team will be available to answer any questions regarding the status of your shipments. We appreciate your patience as we work to improve our logistics and better serve our customers.",
    "question": "Why is the company moving its warehouse?",
    "paraphrased_word": "storage facility",
    "explanation": "製品を保管しておく「warehouse（倉庫）」は、「storage facility（保管施設）」と言い換えられます。"
  },
  {
    "target_word": "Refund",
    "theme": "返品と返金の対応",
    "passage": "Thank you for shopping at 'Urban Electronics.' If you are not completely satisfied with your purchase, you may return the item within 14 days of delivery for a full reimbursement. Please ensure that the product is in its original packaging and that you have the receipt or proof of purchase. Once we receive and inspect the returned item, we will process the payment back to your original credit card within five business days. Please note that shipping costs for returns are the responsibility of the customer unless the item was damaged upon arrival. For more information on our return policy, please visit the 'Support' section of our website or contact our customer service desk.",
    "question": "How can a customer receive a refund?",
    "paraphrased_word": "reimbursement",
    "explanation": "支払った金銭の払い戻し処理を指す「refund」は、「reimbursement（払い戻し）」と言い換えられます。"
  },
  {
    "target_word": "Advise",
    "theme": "旅行の持ち物に関するアドバイス",
    "passage": "Dear Travelers, we are looking forward to our upcoming guided tour of the Swiss Alps! To ensure you have a safe and enjoyable experience, we recommend that you bring sturdy hiking boots and waterproof clothing. The weather in the mountains can change rapidly, so it is best to be prepared for both sun and rain. We also suggest carrying a reusable water bottle and a small backpack for your personal items. Our guide will provide more detailed information during the orientation meeting on the first evening. If you have any specific dietary requirements or medical conditions, please let us know in advance so we can make the necessary arrangements. See you soon!",
    "question": "What does the tour operator advise travelers to bring?",
    "paraphrased_word": "recommend",
    "explanation": "「advise（助言する、勧める）」という行為は、本文中の「recommend（推奨する）」と連動します。"
  },
  {
    "target_word": "Immediately",
    "theme": "緊急のセキュリティ対応",
    "passage": "Attention all employees: We have detected a potential security breach in our internal network system. To protect your data, all staff members are requested to change their login passwords promptly. Please follow the instructions sent to your corporate email to ensure your new password meets the updated security requirements. Do not use personal information or simple numeric sequences. If you encounter any difficulties accessing your account, please contact the IT help desk at extension 405. It is crucial that we address this issue as soon as possible to prevent any unauthorized access to sensitive company information. Thank you for your cooperation in maintaining a secure workplace.",
    "question": "What are employees asked to do immediately?",
    "paraphrased_word": "promptly",
    "explanation": "直ちに行動することを求める「immediately（すぐに）」は、迅速な対応を促す副詞「promptly（速やかに）」に変換されます。"
  },
  {
    "target_word": "Council",
    "theme": "地域の開発計画",
    "passage": "The local committee for urban planning has recently approved the proposal for the new central park project. This decision follows months of community meetings and environmental impact studies. The project aims to create more green space for residents and will include walking paths, a children's playground, and a small outdoor theater. Construction is set to begin next spring, with an expected completion date of late summer. Funding for the park will be provided by a combination of government grants and private donations. A public hearing will be held next Tuesday at the Town Hall to present the final design to the community and answer any remaining questions about the project.",
    "question": "What did the city council recently approve?",
    "paraphrased_word": "committee",
    "explanation": "意思決定機関としての「council（議会）」は、特定の役割を持った代表集団を指す「committee（委員会）」と言い換えられます。"
  },
  {
    "target_word": "Broadcast",
    "theme": "テレビ番組の放送予定",
    "passage": "Don't miss the premiere of our new documentary series, 'Wild Oceans,' which will air this Sunday at 8:00 P.M. on Channel 5. This fascinating program explores the hidden lives of deep-sea creatures and features stunning underwater footage filmed over three years. Each episode will focus on a different region of the world's oceans, from the icy Arctic to the tropical coral reefs. We invite viewers to learn about the challenges facing marine environments and the efforts being made to protect them. For more information on the series and to watch behind-the-scenes clips, please visit our website. Set your recorders now for this must-see television event!",
    "question": "When will the documentary be broadcast?",
    "paraphrased_word": "air",
    "explanation": "番組などを放送することを意味する「broadcast」は、メディアの文脈において「air（放映される）」と言い換えられます。"
  },
  {
    "target_word": "Responsible",
    "theme": "新任マネージャーの職務内容",
    "passage": "We are pleased to welcome Ms. Alice Wong as our new Operations Manager. Alice comes to us with over ten years of experience in the logistics industry. In her new role, she will be in charge of overseeing our daily distribution activities and managing relations with our international suppliers. She will also lead the team in implementing our new inventory tracking software. We are confident that her expertise will help us streamline our processes and improve overall efficiency. Alice will be based at our regional office in Chicago. Please join us for a welcome coffee in the lounge this Friday afternoon to meet Alice and learn more about her vision for the department.",
    "question": "What is Ms. Wong responsible for in her new role?",
    "paraphrased_word": "in charge of",
    "explanation": "「responsible for（〜の責任を負う）」は、最重要熟語表現「in charge of（〜を担当している）」にパラフレーズされます。"
  },
  {
    "target_word": "Avoid",
    "theme": "交通渋滞の回避案内",
    "passage": "Due to major road repairs occurring on the main highway, commuters are advised to use alternative routes to prevent long delays during the morning rush hour. The construction work is expected to last for two weeks, affecting traffic flow in both directions. We recommend using the subway or the regional train service as a more reliable option until the repairs are finished. For real-time updates on road conditions, please download our city's traffic app or check our official social media pages. We apologize for the inconvenience and appreciate your patience as we work to improve our city's infrastructure and ensure a smoother journey for everyone in the future.",
    "question": "What should drivers do to avoid delays?",
    "paraphrased_word": "prevent",
    "explanation": "事態の発生を防ぐ「avoid（避ける）」は、「prevent（防ぐ）」という表現として記述されます。"
  },
  {
    "target_word": "Effective",
    "theme": "新ルールの適用日",
    "passage": "To: All Staff\nFrom: Facilities Management\nSubject: Parking Policy Update\n\nPlease be advised that the new parking regulations for our company lot will be starting next Monday, July 1. Under the updated policy, all employees must display a valid parking permit on their windshield. Permits can be obtained from the security office during regular business hours. Visitors will be required to use the designated guest spots near the main entrance. This change is intended to ensure that enough space is available for all staff members throughout the day. Please make sure to pick up your permit before the weekend to avoid any issues on Monday. Thank you for your cooperation in following these new guidelines.",
    "question": "When will the new parking policy become effective?",
    "paraphrased_word": "starting",
    "explanation": "ルールが実効力を持つ「effective（有効な）」という状態は、日付表現と合わさって「starting（〜より始まる）」と言い換えられます。"
  },
  {
    "target_word": "Invitation",
    "theme": "展示会への招待",
    "passage": "Dear Valued Partner,\n\nWe are pleased to send you this request to attend our upcoming Annual Technology Expo, which will take place on October 15. This exclusive event is an opportunity to see our latest innovations in artificial intelligence and robotics before they are released to the general public. The expo will feature keynote speeches from industry leaders and live demonstrations of our newest products. Refreshments will be served throughout the day, followed by a networking dinner in the evening. Please RSVP by clicking the link below before the end of this month to confirm your attendance. We look forward to seeing you at the exhibition and sharing our vision for the future.",
    "question": "What is the purpose of the invitation sent to the partner?",
    "paraphrased_word": "request to attend",
    "explanation": "「invitation（招待）」は、本文で少し丁寧に「request to attend（参加のお願い）」というフレーズに変形されて記述されています。"
  },
  {
    "target_word": "Reduce",
    "theme": "コスト削減の取り組み",
    "passage": "In our continuous effort to improve profitability, the company has decided to implement new measures to cut operational expenses. Starting next month, we will be transitioning to a more digital workflow to decrease paper consumption and mailing costs. We also plan to upgrade our office lighting to energy-efficient LED systems, which is expected to lower our monthly electricity bills by 15%. All department heads are requested to review their current spending and identify any additional areas where savings can be made. These changes are crucial for maintaining our competitive edge and ensuring long-term financial stability. We appreciate your support in helping us achieve these important goals.",
    "question": "How does the company plan to reduce operational expenses?",
    "paraphrased_word": "cut",
    "explanation": "「reduce（削減する）」という動詞は、「cut（切り詰める）」や「lower」に言い換えられます。"
  },
  {
    "target_word": "Vehicle",
    "theme": "社用車の利用規則",
    "passage": "Employees who are required to drive for business purposes must follow the updated policy regarding the use of a company automobile. Before using any company-owned car, you must record your name, the date, and the starting mileage in the logbook located in the glove compartment. Please ensure that the interior is kept clean and that the fuel tank is at least half full when you return it. In case of an accident or mechanical failure, contact the fleet manager immediately. Personal use of these cars is strictly prohibited. Failure to follow these rules may result in the loss of driving privileges. Thank you for your cooperation and for driving safely at all times.",
    "question": "What must employees do before using a company vehicle?",
    "paraphrased_word": "automobile",
    "explanation": "「vehicle（車両）」は、本文で乗用車を示す「automobile（自動車）」や「car」として具体化されパラフレーズされます。"
  },
  {
    "target_word": "Efficient",
    "theme": "新しい製造プロセスの導入",
    "passage": "Our factory has recently introduced a streamlined assembly process that has significantly improved our production capacity. By reorganizing the layout of the workstations and installing new automated machinery, we can now produce 20% more units per day without increasing labor costs. This improvement allows us to respond faster to customer orders and reduce our lead times. We will hold a training session next Wednesday to familiarize all staff members with the new equipment and safety protocols. We believe that these changes will make our operations more productive and help us maintain our leading position in the market. Thank you for your hard work and adaptability during this transition.",
    "question": "What has made the factory's production more efficient?",
    "paraphrased_word": "streamlined",
    "explanation": "無駄がなく効率的な状態を指す「efficient」は、工程などが合理化されたという意味の「streamlined（能率的な）」に置き換わります。"
  },
  {
    "target_word": "Manufacturer",
    "theme": "新製品の供給元紹介",
    "passage": "At 'Green Living,' we are committed to sourcing our products from the most reliable environmental equipment maker in the industry. Our primary partner, Zenith Eco-Systems, has over 20 years of experience in producing high-quality solar panels and water filtration systems. By working directly with them, we can ensure that our customers receive the latest technology at the best possible price. Zenith is known for its rigorous quality control standards and its focus on sustainable production methods. We are proud to feature their full range of products in our showroom. Visit us today to see how these innovative solutions can help you reduce your carbon footprint and save on energy costs.",
    "question": "Who is the primary manufacturer for Green Living?",
    "paraphrased_word": "maker",
    "explanation": "「manufacturer（製造会社）」は、よりシンプルな名詞表現「maker（製造業者）」と言い換えられます。"
  },
  {
    "target_word": "Comfortable",
    "theme": "ホテルの客室紹介",
    "passage": "Welcome to the Riverside Grand Hotel! We aim to provide a pleasant stay for all our guests by offering a range of premium amenities and exceptional service. Each of our guest rooms is equipped with high-quality linens, adjustable air conditioning, and soundproof windows to ensure a quiet environment. Our goal is to make you feel right at home while you are traveling for business or leisure. We also feature an on-site spa and a heated indoor swimming pool for your relaxation. Our concierge team is available 24/7 to assist with dining reservations or local tour arrangements. We hope you enjoy your time with us and have a truly relaxing experience.",
    "question": "What does the hotel provide to ensure a comfortable stay?",
    "paraphrased_word": "pleasant",
    "explanation": "「comfortable（快適な）」という環境評価は、本文で「pleasant（心地よい）」と言い換えられます。"
  },
  {
    "target_word": "Correct",
    "theme": "請求書の誤りに関する連絡",
    "passage": "Dear Customer, thank you for your recent purchase at Apex Electronics. We are writing to address a potential discrepancy in your latest billing statement. It has come to our attention that some customers were charged twice for shipping. Please review your invoice to ensure all amounts are accurate. If you notice any errors, please contact our support team with your order number. We will issue a refund for any overcharges within three business days. We strive to maintain the highest standards of service and sincerely regret this technical glitch. Thank you for your patience and for choosing us for your technology needs.",
    "question": "What should the customer do to ensure their invoice is correct?",
    "paraphrased_word": "accurate",
    "explanation": "データや数値が「correct（正しい）」という状態は、実務的な表現である「accurate（正確な）」と言い換えられます。"
  },
  {
    "target_word": "Downtown",
    "theme": "店舗の移転案内",
    "passage": "To our valued clients, we are excited to announce that 'The Daily Grind' cafe is moving to a new location! Starting next month, you can find us in the heart of the city center, just steps away from the Grand Plaza. Our new space will offer more seating and an expanded menu of organic teas and pastries. Please note that our current shop will close on Friday evening to prepare for the move. We believe this new spot will be much more convenient for our corporate customers and commuters. We look forward to welcoming you to our grand opening celebration on Monday morning. Free samples will be available for all visitors!",
    "question": "Where is the new cafe located in the downtown area?",
    "paraphrased_word": "city center",
    "explanation": "中心街エリアを示す「downtown」は、本文内で「city center（都市中心部）」として表現されます。"
  },
  {
    "target_word": "Method",
    "theme": "支払い方法の選択",
    "passage": "Thank you for registering for the International Marketing Summit. To finalize your registration, please select your preferred way of payment. We accept all major credit cards, as well as bank transfers and mobile pay options. Please note that a small processing fee may apply depending on your choice. Once the transaction is complete, a confirmation email and a digital receipt will be sent to your registered address. For group bookings of five or more people, a 10% discount is available. Please contact our finance department directly if you require a formal invoice before making the payment. We look forward to seeing you at the summit in November.",
    "question": "What should participants choose as their payment method?",
    "paraphrased_word": "way",
    "explanation": "「method（方法）」という名詞は、日常的な汎用単語である「way（やり方、方法）」へとパラフレーズされます。"
  },
  {
    "target_word": "Entire",
    "theme": "ビル全体の改修工事",
    "passage": "Attention all tenants: Please be advised that the management will be conducting a maintenance inspection of the whole building this Saturday. The process will begin at 8:00 A.M. and is expected to conclude by 5:00 P.M. During this time, there may be brief interruptions to the water and electricity supply. We recommend that you turn off all electronic equipment and store sufficient water for your needs. Security personnel will be on-site to assist with any issues. We apologize for the inconvenience this necessary work may cause and appreciate your cooperation in helping us maintain a safe and functional environment for everyone. Thank you for your understanding.",
    "question": "Will the entire building be inspected on Saturday?",
    "paraphrased_word": "whole",
    "explanation": "「entire（全体の）」の言い換えとして、100%連動するのが重要単語「whole（丸ごとの）」です。"
  },
  {
    "target_word": "Range",
    "theme": "新製品のラインナップ",
    "passage": "Discover the latest collection at 'Lumina Home Decor.' This season, we are proud to introduce a wide variety of handmade lighting fixtures and artisanal furniture. From modern minimalist lamps to classic wooden tables, our new items are designed to suit any interior style. We use sustainable materials to ensure that our products are as eco-friendly as they are beautiful. Visit our showroom this weekend to explore the full collection and receive expert advice from our interior design consultants. Special discounts will be offered on select items during our launch event. Don't miss this chance to transform your living space with our unique and high-quality designs.",
    "question": "What is special about the range of products at the store?",
    "paraphrased_word": "variety",
    "explanation": "品揃えの幅を指す「range」は、種類の豊富さを強調する「variety（多様性）」と言い換えられます。"
  },
  {
    "target_word": "Setting",
    "theme": "職場の環境改善",
    "passage": "At Zenith Solutions, we believe that a productive work environment is essential for our team's success. That is why we are investing in new ergonomic furniture and improved lighting for our main office. These changes aim to create a more comfortable and healthy space for all employees. We are also introducing a flexible desk policy to encourage collaboration between different departments. We value your feedback on these improvements, so please share your thoughts during our next staff meeting. We are committed to fostering a workplace where everyone can perform at their best. Thank you for your hard work and dedication to our company's mission.",
    "question": "What kind of setting is the company trying to improve?",
    "paraphrased_word": "environment",
    "explanation": "背景や設定を意味する「setting」は、職場環境そのものを表す重要語「environment」にマッピングされます。"
  },
  {
    "target_word": "Apologize",
    "theme": "サービスの不具合に対する謝罪",
    "passage": "Dear Subscriber, we have recently experienced technical difficulties with our video streaming service. Some users may have had trouble logging in or experienced buffering issues during peak hours. We are sorry for the disruption and are working hard to resolve these problems as quickly as possible. Our technical team has already implemented several patches to improve stability. As a gesture of goodwill, we have added a one-week credit to your account at no extra charge. We value your business and are dedicated to providing you with the best entertainment experience. Thank you for your continued patience and support as we upgrade our systems.",
    "question": "Why does the company want to apologize to its subscribers?",
    "paraphrased_word": "sorry",
    "explanation": "「apologize（謝罪する）」という行為は、本文中で「sorry（申し訳なく思う）」という表現で示されます。"
  },
  {
    "target_word": "Frequent",
    "theme": "定期的な出張者向け特典",
    "passage": "Travel more and save more with the 'Elite Traveler' program! Our new loyalty scheme is designed specifically for regular passengers who use our airline for business trips. Members can earn points for every mile flown, which can be redeemed for seat upgrades, extra baggage allowance, or even free flights. Additionally, you will receive priority boarding and access to our exclusive airport lounges worldwide. Sign up today on our website or at any check-in counter to start enjoying these benefits. It is our way of saying thank you to our most loyal customers. Join the elite group of travelers who choose Pacific Airways for their global journeys.",
    "question": "Who can benefit from the frequent traveler program?",
    "paraphrased_word": "regular",
    "explanation": "度重なる利用を表す「frequent（頻繁な）」は、定期的なリピーターを指す「regular（定期的な）」にマッピングされます。"
  },
  {
    "target_word": "Promotion",
    "theme": "期間限定の特別セール",
    "passage": "Summer is almost here, and it's time to upgrade your outdoor gear! 'Peak Performance' is excited to announce a special offer on all camping and hiking equipment. For a limited time, when you buy two items, you will get the third one for free. This deal applies to tents, backpacks, and sleeping bags. Visit our store this weekend to browse our new arrivals and take advantage of these incredible savings. Our expert staff are available to help you find the perfect gear for your next adventure. Don't wait too long, as stocks are limited and this event ends on Sunday evening. See you at Peak Performance!",
    "question": "What does the promotion at the store include?",
    "paraphrased_word": "special offer",
    "explanation": "販促キャンペーンとしての「promotion」は、具体的な「special offer（特別プラン）」と言い換えられます。"
  },
  {
    "target_word": "Regarding",
    "theme": "新ポリシーに関する通知",
    "passage": "To: All Project Managers\nFrom: Operations Director\nSubject: Expense Reporting\n\nPlease be advised that we have updated the internal guidelines concerning business travel expenses. These changes are intended to simplify the reimbursement process and ensure transparency across all departments. The new forms can be found on the company intranet under the 'Finance' tab. Please ensure that all receipts are scanned and attached to your digital claims. If you have any questions about the specific categories or limits, please attend the brief information session this Friday at 2:00 P.M. It is essential that everyone follows these updated protocols to avoid any delays in payment. Thank you for your cooperation.",
    "question": "What is the notice regarding?",
    "paraphrased_word": "concerning",
    "explanation": "「regarding（〜に関して）」の言い換えとして重要な前置詞は「concerning」です。"
  },
  {
    "target_word": "Temporary",
    "theme": "一時的な通行止め",
    "passage": "Public Notice: Road Maintenance on West Street\n\nStarting Monday, November 12, there will be a short-term closure of the North Bridge due to structural repairs. This project is expected to last for five days, weather permitting. During this time, motorists are advised to use the South Bridge as an alternative route. We apologize for any inconvenience and appreciate your patience as we work to ensure the safety of our city's infrastructure. Pedestrian access will remain open, but please follow the signs and directions from on-site staff. We aim to complete the work as quickly as possible and will provide another update once the bridge is fully reopened to traffic.",
    "question": "Is the closure of the bridge temporary?",
    "paraphrased_word": "short-term",
    "explanation": "「temporary（一時的な）」は、期間の限定性を示す「short-term（短期的な）」と言い換えられます。"
  },
  {
    "target_word": "Traditional",
    "theme": "伝統料理のレストラン案内",
    "passage": "Experience the authentic flavors of Italy at 'Mama's Kitchen.' We take pride in using conventional recipes passed down through generations to create our signature pasta dishes and desserts. Our chefs use only the freshest locally sourced ingredients to ensure every meal is a true culinary delight. Whether you are looking for a romantic dinner or a family celebration, our cozy atmosphere and friendly service will make you feel right at home. We also offer a selection of fine wines to complement your meal. Visit us today and discover why we have been a local favorite for over thirty years. Reservations are recommended for weekend evenings.",
    "question": "What kind of cooking does the traditional restaurant offer?",
    "paraphrased_word": "conventional",
    "explanation": "「traditional（伝統的な）」は、古くからの手法を意味する「conventional（従来の）」という形容詞にリンクすることがあります。"
  },
  {
    "target_word": "Admission",
    "theme": "博物館の入館料",
    "passage": "Welcome to the City Art Museum! We are open Tuesday through Sunday from 10:00 A.M. to 6:00 P.M. For all visitors, the entry fee is $15 for adults and $10 for students and seniors. Children under the age of 12 can enter for free. Please note that special exhibitions may require an additional ticket. We also offer group discounts for parties of ten or more people; please contact our office in advance to arrange a group visit. Your ticket includes access to our permanent collection and a guided tour of the main gallery held every afternoon at 2:00 P.M. We hope you enjoy your visit and find inspiration in our diverse collection.",
    "question": "How much is the admission for students?",
    "paraphrased_word": "entry fee",
    "explanation": "「admission（入場料）」にかかるコストは、ストレートな表現である「entry fee」にパラフレーズされます。"
  },
  {
    "target_word": "Fit",
    "theme": "求職者の適性判断",
    "passage": "Dear Mr. Wallace, thank you for coming to our office yesterday for the interview. Our team was impressed by your technical skills and your experience in project management. We believe that your background in software development makes you a suitable candidate for our engineering department. We are particularly interested in your work with mobile applications and your ability to lead a diverse team. We will be making our final decision by the end of this week and will notify all applicants via email. In the meantime, if you have any further questions or would like to provide additional references, please feel free to contact us. We appreciate your interest in joining our firm.",
    "question": "Does the hiring manager think Mr. Wallace is a good fit for the position?",
    "paraphrased_word": "suitable",
    "explanation": "「fit（適した）」は、フォーマルな文脈で「suitable（ふさわしい）」と言い換えられます。"
  },
  {
    "target_word": "Reference",
    "theme": "採用時の照会先確認",
    "passage": "To apply for the Senior Accountant position, please submit your resume and a brief cover letter. In your letter, please include the contact information for at least two professional recommendation providers who can speak to your work history and character. We will only contact these individuals if you are selected for the final round of interviews. Please ensure that you have informed your former supervisors before including their names in your application. Additionally, a copy of your university transcripts and any relevant certifications should be attached. We look forward to reviewing your application and learning more about your professional achievements in the field of finance.",
    "question": "What information should be included for the job reference?",
    "paraphrased_word": "recommendation",
    "explanation": "推薦を担う集団や書類を指す「reference」は、「recommendation」と言い換えられます。"
  },
  {
    "target_word": "Status",
    "theme": "配送状況の確認",
    "passage": "Dear Customer, thank you for your order with 'EcoWorld.' This email is to inform you that your package has been shipped and is currently in transit. You can check the current progress of your delivery by clicking the link below or by entering your tracking number on our website. Please note that it may take up to 24 hours for the carrier's system to update the information. Most domestic orders are delivered within three to five business days. If you are not available to receive the package, the courier will leave a notice with instructions for redelivery. We appreciate your business and hope you enjoy your new sustainable products.",
    "question": "Where can the customer check the status of their order?",
    "paraphrased_word": "progress",
    "explanation": "荷物の配送などの「status（状況）」は、進み具合を意味する「progress（進捗）」と言い換えられます。"
  },
  {
    "target_word": "Fuel",
    "theme": "レンタカーの返却ルール",
    "passage": "Thank you for choosing 'EasyDrive' for your car rental needs. To ensure a smooth return process, please remember to fill the tank with gasoline before bringing the vehicle back to our office. If the car is returned with less than a full tank, a refueling fee will be added to your final bill. Please use the designated return lane and leave the keys with one of our staff members. Also, ensure that all personal items have been removed from the interior. If you need to extend your rental period, please contact us at least 24 hours in advance to check for availability. We hope you have a safe and pleasant journey with our rental car.",
    "question": "What must the customer do regarding the fuel before returning the car?",
    "paraphrased_word": "gasoline",
    "explanation": "「fuel（燃料）」は、自動車の利用文脈において「gasoline（ガソリン）」と言い換えられます。"
  },
  {
    "target_word": "Nearly",
    "theme": "プロジェクトの完了間近",
    "passage": "To: All Staff\nFrom: Project Lead\nSubject: Website Redesign Update\n\nI am happy to report that the redesign of our corporate website is almost complete. The development team has finished the new layout and is currently testing the user interface on different mobile devices. We expect to launch the new site by next Friday, assuming no major technical issues are discovered during the final review. Please take a look at the preview version and send your feedback to the design team by Tuesday afternoon. This project represents a significant step in our digital strategy, and I want to thank everyone for their hard work and creativity throughout the process. We are very close to reaching our goal!",
    "question": "Is the website project nearly finished?",
    "paraphrased_word": "almost",
    "explanation": "「nearly（ほとんど）」の最も鉄板となるパラフレーズ表記は「almost」です。"
  },
  {
    "target_word": "Cafeteria",
    "theme": "社内食堂のメニュー変更",
    "passage": "Attention Employees: We are pleased to announce that our staff dining hall will be introducing a new healthy menu starting next week. The updated selection will include more vegetarian options, fresh salads, and low-sodium soups. To celebrate the launch, we will be offering a free fruit smoothie with every meal purchased on Monday. We have also extended our opening hours during the lunch period to reduce waiting times. Please remember to use the digital kiosks to place your orders more quickly. We hope these changes will provide you with more nutritious and convenient lunch options. Your feedback on the new dishes is always welcome!",
    "question": "What is being changed in the company cafeteria?",
    "paraphrased_word": "dining hall",
    "explanation": "施設内の食堂を指す「cafeteria」は、社内の食事スペースを表す「dining hall」と言い換えられます。"
  },
  {
    "target_word": "Determine",
    "theme": "市場調査による価格設定",
    "passage": "Before we launch our new smartwatch, we need to conduct a comprehensive market study to find out the most competitive price point. Our research team will gather data from potential customers regarding their budget and preferred features. We will also analyze the pricing strategies of our main competitors in the consumer electronics sector. Once this information is collected, we will hold a meeting to set the final retail price for our product. This careful analysis is crucial for ensuring that our launch is successful and that we achieve our sales targets for the first quarter. We appreciate your cooperation in providing the necessary data for this important task.",
    "question": "What is the company trying to determine through research?",
    "paraphrased_word": "find out",
    "explanation": "「determine（決定する）」という分析動作は、平易な表現である「find out（見出し、解明する）」と言い換えられます。"
  }
]

# アプリケーションのグローバル状態管理（セッションステート）
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "is_answered" not in st.session_state:
    st.session_state.is_answered = False
if "selected_sentence" not in st.session_state:
    st.session_state.selected_sentence = None
if "is_correct" not in st.session_state:
    st.session_state.is_correct = False

# 現在の問題データ
q = st.session_state.question_data[st.session_state.current_index]

# 200単語のカウントアップ
total_questions = len(st.session_state.question_data)

# --- 文単位の選択肢自動生成システム ---
clean_passage = q["passage"].replace('\n', ' ')
sentences = re.split(r'(?<=[.!?])\s+', clean_passage)
sentences = [s.strip() for s in sentences if s.strip()]

target_phrase_raw = q["paraphrased_word"].strip()
final_sentences_options = sorted(list(set(sentences)))

# --- 画面表示部 ---
progress_val = (st.session_state.current_index + 1) / total_questions
st.progress(progress_val)
st.caption(f"Question {st.session_state.current_index + 1} / {total_questions}")

# メインコンテナ構造
with st.container():
    st.markdown(f'<div class="target-badge">Target Word: {q["target_word"].upper()}</div>', unsafe_allow_html=True)
    st.subheader(f"Q. {q['question']}")
    st.info("💡 設問内のターゲットキーワードの『言い換え表現』が含まれている正しい文エリアを、下の選択肢から選んでください。")

# 本文の出力
st.markdown("#### 【英文テキスト】")
st.markdown(f'<div class="toeic-passage-box">{q["passage"]}</div>', unsafe_allow_html=True)

# 文単位セレクトUI
st.markdown("#### 【スキャニング選択（文単位）】")
selected_choice = st.selectbox(
    "言い換え語を含んでいる『正確な一文』をリストから丸ごと選択してください：",
    ["選択してください..."] + final_sentences_options,
    key=f"sc_select_{st.session_state.current_index}"
)

# 判定用の特殊記号クレンジング関数
def clean_normalize_text(text_str):
    return re.sub(r"[.,\/#!$%\^&\*;:{}=\-_`~()]", "", text_str).lower().strip()

# 正誤判定処理
if selected_choice != "選択してください..." and not st.session_state.is_answered:
    st.session_state.selected_sentence = selected_choice
    st.session_state.is_answered = True
    
    clean_target_keyword = clean_normalize_text(target_phrase_raw)
    clean_user_selected_sentence = clean_normalize_text(selected_choice)
    
    if clean_target_keyword in clean_user_selected_sentence:
        st.session_state.is_correct = True
    else:
        st.session_state.is_correct = False

# 判定結果と解説カード表示
if st.session_state.is_answered:
    actual_correct_sentence = ""
    for s_opt in final_sentences_options:
        if clean_normalize_text(target_phrase_raw) in clean_normalize_text(s_opt):
            actual_correct_sentence = s_opt
            break
            
    if st.session_state.is_correct:
        st.success(f"🎉 **正解です！** 正確な言い換え表現「{target_phrase_raw}」が格納されている文エリアを完璧に見抜きました！")
    else:
        st.error(f"❌ **不正解！** 単語の一部ではなく、正しいフレーズが含まれる文エリアを捉えきれませんでした。")
        st.info(f"💡 **正解となる文（Area）:** \n\n「 *{actual_correct_sentence}* 」\n\n（この中に **{target_phrase_raw}** が仕込まれていました）")
        
    st.markdown("### 💡 スキャニング予測のコツ（解説）")
    st.write(q["explanation"])
    
    # 次の問題への移動処理
    if st.button("次の問題へ移動する ➡️", type="primary"):
        if st.session_state.current_index + 1 < total_questions:
            st.session_state.current_index += 1
        else:
            st.balloons()
            st.success("素晴らしい！全200単語のスキャニング訓練をすべて完遂しました！")
            st.session_state.current_index = 0
            
        st.session_state.is_answered = False
        st.session_state.selected_sentence = None
        st.session_state.is_correct = False
        st.rerun()
