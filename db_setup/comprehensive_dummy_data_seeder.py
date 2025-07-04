import openai
import random
from supabase import create_client
from tqdm import tqdm
import json
import time
from config import SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY, EMBEDDING_MODEL

# Initialize clients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def embed_text(text: str):
    """Generate embedding for text with error handling."""
    try:
        response = openai_client.embeddings.create(
            input=[text],
            model=EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding failed: {e}")
        return [0.0] * 1536  # fallback dummy embedding


def safe_insert(table_name, data):
    """Safely insert data with error handling."""
    try:
        result = supabase.table(table_name).insert(data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Insert failed for {table_name}: {e}")
        return None


# Course definitions with detailed content
COURSES_DATA = {
    "Machine Learning": {
        "description": """Comprehensive machine learning course covering supervised and unsupervised learning algorithms, 
        neural networks, deep learning, natural language processing, computer vision, and practical implementation using 
        Python, scikit-learn, TensorFlow, and PyTorch. Students will learn statistical foundations, feature engineering, 
        model evaluation, hyperparameter tuning, and deployment strategies for real-world ML applications.""",
        "tasks": [
            "Implement linear regression from scratch using Python and NumPy",
            "Build a decision tree classifier for the Iris dataset",
            "Create a k-means clustering algorithm to segment customer data",
            "Develop a neural network for handwritten digit recognition (MNIST)",
            "Build a recommendation system using collaborative filtering",
            "Implement gradient descent optimization algorithm",
            "Create a support vector machine for text classification",
            "Build a random forest model for predicting house prices",
            "Develop a CNN for image classification using TensorFlow",
            "Implement a recurrent neural network for sentiment analysis",
            "Create a reinforcement learning agent for a simple game",
            "Build an ensemble model combining multiple algorithms",
            "Develop a feature selection pipeline using various techniques",
            "Implement cross-validation and hyperparameter tuning",
            "Create a time series forecasting model using LSTM",
            "Build a generative adversarial network (GAN) for image generation",
            "Develop a natural language processing pipeline for text analysis",
            "Implement principal component analysis (PCA) for dimensionality reduction",
            "Create a model for anomaly detection in network traffic",
            "Build a multi-class classification system for document categorization",
            "Develop a regression model with regularization techniques",
            "Implement a naive Bayes classifier for spam detection",
            "Create a clustering analysis for market segmentation",
            "Build a predictive model for stock price movements",
            "Develop a computer vision system for object detection",
            "Implement a recommendation engine using matrix factorization",
            "Create a model interpretability dashboard using SHAP",
            "Build a real-time ML pipeline using Apache Kafka",
            "Develop a federated learning system for privacy-preserving ML",
            "Implement AutoML pipeline for automated model selection"
        ],
        "resources": [
            {"title": "Scikit-learn Official Documentation", "url": "https://scikit-learn.org/",
             "tags": ["documentation", "python", "library"]},
            {"title": "TensorFlow Machine Learning Platform", "url": "https://tensorflow.org/",
             "tags": ["deep-learning", "neural-networks", "google"]},
            {"title": "PyTorch Deep Learning Framework", "url": "https://pytorch.org/",
             "tags": ["deep-learning", "research", "facebook"]},
            {"title": "Kaggle Learn Machine Learning Course", "url": "https://kaggle.com/learn/",
             "tags": ["interactive", "datasets", "competitions"]},
            {"title": "Andrew Ng's Machine Learning Course", "url": "https://coursera.org/learn/machine-learning",
             "tags": ["stanford", "fundamentals", "theory"]},
            {"title": "Python Machine Learning Book by Sebastian Raschka",
             "url": "https://github.com/rasbt/python-machine-learning-book",
             "tags": ["book", "practical", "algorithms"]},
            {"title": "Google's Machine Learning Crash Course",
             "url": "https://developers.google.com/machine-learning/crash-course",
             "tags": ["google", "free", "tensorflow"]},
            {"title": "MLflow - ML Lifecycle Management", "url": "https://mlflow.org/",
             "tags": ["mlops", "tracking", "deployment"]},
            {"title": "Weights & Biases - Experiment Tracking", "url": "https://wandb.ai/",
             "tags": ["experiment-tracking", "visualization", "collaboration"]},
            {"title": "Papers With Code - Latest ML Research", "url": "https://paperswithcode.com/",
             "tags": ["research", "papers", "implementations"]},
            {"title": "Distill - Visual Explanations of ML Concepts", "url": "https://distill.pub/",
             "tags": ["visualization", "explanations", "interactive"]},
            {"title": "Towards Data Science Medium Publication", "url": "https://towardsdatascience.com/",
             "tags": ["articles", "tutorials", "community"]},
            {"title": "Machine Learning Mastery Blog", "url": "https://machinelearningmastery.com/",
             "tags": ["tutorials", "practical", "jason-brownlee"]},
            {"title": "UCI Machine Learning Repository", "url": "https://archive.ics.uci.edu/ml/",
             "tags": ["datasets", "benchmark", "research"]},
            {"title": "Google Colab - Free GPU Computing", "url": "https://colab.research.google.com/",
             "tags": ["jupyter", "gpu", "cloud"]},
            {"title": "Jupyter Notebooks for Data Science", "url": "https://jupyter.org/",
             "tags": ["interactive", "python", "data-analysis"]},
            {"title": "Anaconda Python Distribution", "url": "https://anaconda.com/",
             "tags": ["python", "package-manager", "data-science"]},
            {"title": "OpenAI GPT Models and API", "url": "https://openai.com/api/",
             "tags": ["language-models", "api", "gpt"]},
            {"title": "Hugging Face Transformers Library", "url": "https://huggingface.co/transformers/",
             "tags": ["nlp", "transformers", "pretrained-models"]},
            {"title": "Fast.ai Practical Deep Learning Course", "url": "https://fast.ai/",
             "tags": ["practical", "deep-learning", "accessibility"]},
            {"title": "CS229 Stanford Machine Learning Notes", "url": "http://cs229.stanford.edu/",
             "tags": ["stanford", "theory", "mathematical"]},
            {"title": "Pattern Recognition and Machine Learning Book",
             "url": "https://www.microsoft.com/en-us/research/people/cmbishop/",
             "tags": ["textbook", "theory", "bayesian"]},
            {"title": "Elements of Statistical Learning Book", "url": "https://web.stanford.edu/~hastie/ElemStatLearn/",
             "tags": ["statistics", "theory", "comprehensive"]},
            {"title": "Machine Learning Yearning by Andrew Ng", "url": "https://www.mlyearning.org/",
             "tags": ["strategy", "practical-advice", "project-management"]},
            {"title": "Google AI Research Publications", "url": "https://ai.google/research/",
             "tags": ["research", "cutting-edge", "publications"]},
            {"title": "MIT OpenCourseWare Machine Learning", "url": "https://ocw.mit.edu/",
             "tags": ["mit", "free", "academic"]},
            {"title": "Machine Learning Algorithms Cheat Sheet", "url": "https://ml-cheatsheet.readthedocs.io/",
             "tags": ["reference", "algorithms", "quick-lookup"]},
            {"title": "Keras Deep Learning Library", "url": "https://keras.io/",
             "tags": ["deep-learning", "high-level", "tensorflow"]},
            {"title": "XGBoost Gradient Boosting Framework", "url": "https://xgboost.readthedocs.io/",
             "tags": ["gradient-boosting", "performance", "competitions"]},
            {"title": "Apache Spark MLlib", "url": "https://spark.apache.org/mllib/",
             "tags": ["big-data", "distributed", "scala"]}
        ]
    },
    "Machine Design": {
        "description": """Advanced mechanical engineering course focusing on machine design principles, stress analysis, 
        material selection, mechanical components design, CAD modeling, finite element analysis, manufacturing 
        considerations, reliability engineering, and optimization techniques. Students will use SolidWorks, ANSYS, 
        and MATLAB for design simulation and analysis of gears, bearings, shafts, springs, and complex machinery.""",
        "tasks": [
            "Design a helical gear system for a specific torque and speed requirement",
            "Perform stress analysis on a cantilever beam using finite element methods",
            "Create a CAD model of a mechanical coupling using SolidWorks",
            "Design and analyze a compression spring for automotive suspension",
            "Calculate bearing life and selection for a rotating machinery application",
            "Design a shaft with multiple loading conditions and safety factors",
            "Perform fatigue analysis on a connecting rod using S-N curves",
            "Create a kinematic analysis of a four-bar linkage mechanism",
            "Design a belt drive system with proper tensioning and alignment",
            "Analyze thermal stresses in a heat exchanger component",
            "Design a pressure vessel according to ASME standards",
            "Perform vibration analysis on a rotating shaft system",
            "Create a failure mode and effects analysis (FMEA) for a gearbox",
            "Design a cam-follower system for specific motion requirements",
            "Analyze buckling stability of a column under compression",
            "Design a welded joint with appropriate safety factors",
            "Create a tolerance analysis for an assembly of mechanical parts",
            "Design a clutch system for automotive transmission",
            "Perform modal analysis on a machine frame structure",
            "Design a pneumatic actuator system with control valves",
            "Analyze contact stresses in gear teeth meshing",
            "Create a reliability prediction model for a mechanical system",
            "Design a heat sink for electronic component cooling",
            "Perform optimization of a truss structure for minimum weight",
            "Design a universal joint for power transmission",
            "Analyze creep behavior in high-temperature components",
            "Create a preventive maintenance schedule for industrial machinery",
            "Design a flywheel for energy storage applications",
            "Perform computational fluid dynamics analysis on a pump impeller",
            "Design a robotic joint with actuators and sensors"
        ],
        "resources": [
            {"title": "SolidWorks CAD Software", "url": "https://solidworks.com/",
             "tags": ["cad", "3d-modeling", "simulation"]},
            {"title": "ANSYS Finite Element Analysis", "url": "https://ansys.com/",
             "tags": ["fea", "simulation", "stress-analysis"]},
            {"title": "AutoCAD Design Software", "url": "https://autodesk.com/autocad",
             "tags": ["2d-drafting", "technical-drawing", "industry-standard"]},
            {"title": "Machinery's Handbook", "url": "https://www.industrialpress.com/",
             "tags": ["reference", "machining", "manufacturing"]},
            {"title": "Shigley's Mechanical Engineering Design", "url": "https://mcgraw-hill.com/",
             "tags": ["textbook", "design-theory", "mechanical"]},
            {"title": "ASME Standards and Codes", "url": "https://asme.org/codes-standards",
             "tags": ["standards", "codes", "pressure-vessels"]},
            {"title": "MatWeb Material Property Database", "url": "https://matweb.com/",
             "tags": ["materials", "properties", "database"]},
            {"title": "SKF Bearing Calculator", "url": "https://skf.com/",
             "tags": ["bearings", "calculation", "selection"]},
            {"title": "Boston Gear Design Tools", "url": "https://bostongear.com/",
             "tags": ["gears", "design-tools", "calculations"]},
            {"title": "Engineering Toolbox", "url": "https://engineeringtoolbox.com/",
             "tags": ["calculations", "reference", "formulas"]},
            {"title": "NASA Technical Reports", "url": "https://ntrs.nasa.gov/",
             "tags": ["research", "aerospace", "technical-reports"]},
            {"title": "NIST Material Data", "url": "https://nist.gov/mml",
             "tags": ["standards", "material-data", "research"]},
            {"title": "Fundamentals of Machine Elements", "url": "https://wiley.com/",
             "tags": ["textbook", "machine-elements", "design"]},
            {"title": "MATLAB Simulink for Mechanical Systems", "url": "https://mathworks.com/",
             "tags": ["simulation", "modeling", "control-systems"]},
            {"title": "GrabCAD Community and Models", "url": "https://grabcad.com/",
             "tags": ["cad-models", "community", "free-downloads"]},
            {"title": "Engineering Stress Analysis Textbook", "url": "https://pearson.com/",
             "tags": ["stress-analysis", "theory", "academic"]},
            {"title": "McMaster-Carr Supplier Catalog", "url": "https://mcmaster.com/",
             "tags": ["parts", "components", "specifications"]},
            {"title": "Machine Design Magazine", "url": "https://machinedesign.com/",
             "tags": ["industry-news", "trends", "applications"]},
            {"title": "Roark's Formulas for Stress and Strain", "url": "https://mcgraw-hill.com/",
             "tags": ["stress-formulas", "reference", "calculations"]},
            {"title": "FEA Software Comparison Guide", "url": "https://caeassistant.com/",
             "tags": ["software-comparison", "fea", "selection-guide"]},
            {"title": "Design of Machine Elements by Spotts", "url": "https://pearson.com/",
             "tags": ["machine-elements", "design-methodology", "textbook"]},
            {"title": "Mechanical Vibrations Theory by Thomson", "url": "https://pearson.com/",
             "tags": ["vibrations", "dynamics", "theory"]},
            {"title": "Heat Transfer in Engineering by Holman", "url": "https://mcgraw-hill.com/",
             "tags": ["heat-transfer", "thermal-analysis", "engineering"]},
            {"title": "Manufacturing Processes Reference Guide", "url": "https://wiley.com/",
             "tags": ["manufacturing", "processes", "production"]},
            {"title": "ISO Standards for Mechanical Engineering", "url": "https://iso.org/",
             "tags": ["international-standards", "quality", "specifications"]},
            {"title": "COMSOL Multiphysics Simulation", "url": "https://comsol.com/",
             "tags": ["multiphysics", "simulation", "advanced-analysis"]},
            {"title": "Adams Multibody Dynamics", "url": "https://hexagon.com/",
             "tags": ["dynamics", "multibody", "motion-analysis"]},
            {"title": "Pro/ENGINEER (Creo) CAD System", "url": "https://ptc.com/",
             "tags": ["parametric-design", "cad", "product-development"]},
            {"title": "Mechanical Engineering Design Handbook", "url": "https://crcpress.com/",
             "tags": ["handbook", "comprehensive", "reference"]},
            {"title": "Finite Element Method in Engineering", "url": "https://elsevier.com/",
             "tags": ["fem", "numerical-methods", "advanced-analysis"]}
        ]
    },
    "Economics": {
        "description": """Comprehensive economics course covering microeconomics, macroeconomics, econometrics, behavioral 
        economics, international trade, monetary policy, fiscal policy, development economics, and economic modeling. 
        Students will analyze market structures, economic indicators, policy impacts, and use statistical software 
        like R, Stata, and Python for economic data analysis and forecasting.""",
        "tasks": [
            "Analyze supply and demand curves for a specific market scenario",
            "Calculate price elasticity of demand using real market data",
            "Build an econometric model to predict inflation rates",
            "Perform cost-benefit analysis for a public infrastructure project",
            "Create a game theory analysis of oligopoly market behavior",
            "Analyze the impact of minimum wage policies on employment",
            "Build a macroeconomic model using IS-LM framework",
            "Perform regression analysis on GDP growth factors",
            "Analyze comparative advantage in international trade",
            "Create a monetary policy impact assessment",
            "Build a consumer choice model with utility maximization",
            "Analyze market efficiency using welfare economics",
            "Create a business cycle analysis using historical data",
            "Perform time series analysis of stock market volatility",
            "Analyze income inequality using Gini coefficient calculations",
            "Build a labor market equilibrium model",
            "Create a foreign exchange rate prediction model",
            "Analyze fiscal multiplier effects on economic growth",
            "Perform behavioral economics experiment design and analysis",
            "Build a development economics model for poverty reduction",
            "Analyze market failure scenarios and policy interventions",
            "Create an environmental economics cost analysis",
            "Perform panel data analysis on cross-country economic indicators",
            "Build a housing market bubble detection model",
            "Analyze cryptocurrency market dynamics and volatility",
            "Create a economic impact assessment of technology adoption",
            "Perform central bank policy effectiveness analysis",
            "Build a economic forecasting model using machine learning",
            "Analyze trade war impacts using gravity models",
            "Create a economic dashboard for real-time monitoring"
        ],
        "resources": [
            {"title": "Federal Reserve Economic Data (FRED)", "url": "https://fred.stlouisfed.org/",
             "tags": ["data", "monetary-policy", "economic-indicators"]},
            {"title": "World Bank Open Data", "url": "https://data.worldbank.org/",
             "tags": ["development", "global-data", "statistics"]},
            {"title": "International Monetary Fund Data", "url": "https://imf.org/data",
             "tags": ["international", "macroeconomics", "policy"]},
            {"title": "OECD Statistics and Data", "url": "https://oecd.org/statistics/",
             "tags": ["developed-countries", "policy-analysis", "statistics"]},
            {"title": "R for Econometrics and Statistics", "url": "https://r-project.org/",
             "tags": ["statistical-software", "econometrics", "open-source"]},
            {"title": "Stata Statistical Software", "url": "https://stata.com/",
             "tags": ["econometrics", "data-analysis", "professional"]},
            {"title": "EViews Econometric Software", "url": "https://eviews.com/",
             "tags": ["time-series", "forecasting", "econometrics"]},
            {"title": "Principles of Economics by Mankiw", "url": "https://cengage.com/",
             "tags": ["textbook", "introductory", "principles"]},
            {"title": "Microeconomic Theory by Mas-Colell", "url": "https://oxford.edu/",
             "tags": ["advanced", "microeconomics", "theory"]},
            {"title": "Macroeconomics by Blanchard", "url": "https://pearson.com/",
             "tags": ["macroeconomics", "policy", "analysis"]},
            {"title": "Econometric Analysis by Greene", "url": "https://pearson.com/",
             "tags": ["econometrics", "statistical-methods", "advanced"]},
            {"title": "Bureau of Economic Analysis (BEA)", "url": "https://bea.gov/",
             "tags": ["us-economy", "gdp", "national-accounts"]},
            {"title": "Congressional Budget Office Reports", "url": "https://cbo.gov/",
             "tags": ["fiscal-policy", "budget-analysis", "projections"]},
            {"title": "National Bureau of Economic Research", "url": "https://nber.org/",
             "tags": ["research", "working-papers", "academic"]},
            {"title": "American Economic Association", "url": "https://aeaweb.org/",
             "tags": ["professional", "journals", "conferences"]},
            {"title": "The Economist Intelligence Unit", "url": "https://eiu.com/",
             "tags": ["analysis", "forecasting", "country-risk"]},
            {"title": "Trading Economics Data Portal", "url": "https://tradingeconomics.com/",
             "tags": ["real-time-data", "indicators", "forecasts"]},
            {"title": "Khan Academy Economics Course", "url": "https://khanacademy.org/economics",
             "tags": ["free", "video-lessons", "basics"]},
            {"title": "Coursera Economics Specializations", "url": "https://coursera.org/",
             "tags": ["online-courses", "university-level", "certificates"]},
            {"title": "MIT OpenCourseWare Economics", "url": "https://ocw.mit.edu/",
             "tags": ["mit", "free", "lecture-notes"]},
            {"title": "Economic Policy Institute Research", "url": "https://epi.org/",
             "tags": ["policy-research", "labor", "inequality"]},
            {"title": "Brookings Institution Economics", "url": "https://brookings.edu/",
             "tags": ["think-tank", "policy", "research"]},
            {"title": "Peterson Institute for International Economics", "url": "https://piie.com/",
             "tags": ["international-trade", "policy", "research"]},
            {"title": "Yahoo Finance Economic Data", "url": "https://finance.yahoo.com/",
             "tags": ["financial-markets", "economic-calendar", "real-time"]},
            {"title": "Google Public Data Explorer", "url": "https://google.com/publicdata/",
             "tags": ["visualization", "public-data", "interactive"]},
            {"title": "Quandl Financial and Economic Data", "url": "https://quandl.com/",
             "tags": ["api", "financial-data", "time-series"]},
            {"title": "European Central Bank Statistics", "url": "https://ecb.europa.eu/",
             "tags": ["european-economy", "monetary-policy", "euro"]},
            {"title": "Bank for International Settlements", "url": "https://bis.org/",
             "tags": ["central-banking", "financial-stability", "international"]},
            {"title": "Economic History Association", "url": "https://eh.net/",
             "tags": ["economic-history", "historical-data", "research"]},
            {"title": "Gapminder World Data", "url": "https://gapminder.org/",
             "tags": ["global-development", "visualization", "trends"]}
        ]
    },
    "Web Development": {
        "description": """Full-stack web development course covering HTML5, CSS3, JavaScript ES6+, React.js, Node.js, 
        Express.js, databases (SQL and NoSQL), RESTful APIs, GraphQL, responsive design, web security, testing, 
        deployment, DevOps, and modern development tools. Students will build complete web applications using 
        modern frameworks and best practices for scalable, maintainable code.""",
        "tasks": [
            "Create a responsive landing page using HTML5 and CSS3 flexbox",
            "Build a interactive todo application using vanilla JavaScript",
            "Develop a React.js component library with reusable UI elements",
            "Create a Node.js REST API with Express.js and MongoDB",
            "Build a user authentication system with JWT tokens",
            "Implement a real-time chat application using Socket.io",
            "Create a e-commerce website with shopping cart functionality",
            "Build a progressive web app (PWA) with offline capabilities",
            "Develop a GraphQL API with queries and mutations",
            "Create a responsive blog platform with CMS functionality",
            "Build a social media dashboard using React and Redux",
            "Implement server-side rendering with Next.js",
            "Create a file upload system with image processing",
            "Build a weather application consuming third-party APIs",
            "Develop a task management system with drag-and-drop",
            "Create a multi-language website with internationalization",
            "Build a payment integration using Stripe API",
            "Implement automated testing with Jest and Cypress",
            "Create a containerized application using Docker",
            "Build a microservices architecture with API gateway",
            "Develop a content management system with admin panel",
            "Create a real-time collaborative editor",
            "Build a data visualization dashboard with D3.js",
            "Implement OAuth authentication with Google and Facebook",
            "Create a search functionality with Elasticsearch",
            "Build a notification system with push notifications",
            "Develop a video streaming platform with adaptive bitrate",
            "Create a CI/CD pipeline using GitHub Actions",
            "Build a serverless application using AWS Lambda",
            "Implement web security best practices and OWASP guidelines"
        ],
        "resources": [
            {"title": "Mozilla Developer Network (MDN)", "url": "https://developer.mozilla.org/",
             "tags": ["documentation", "web-standards", "comprehensive"]},
            {"title": "React.js Official Documentation", "url": "https://reactjs.org/",
             "tags": ["react", "frontend", "components"]},
            {"title": "Node.js Official Website", "url": "https://nodejs.org/",
             "tags": ["backend", "javascript", "server"]},
            {"title": "Express.js Web Framework", "url": "https://expressjs.com/",
             "tags": ["nodejs", "backend", "api"]},
            {"title": "MongoDB Database", "url": "https://mongodb.com/", "tags": ["nosql", "database", "document"]},
            {"title": "PostgreSQL Relational Database", "url": "https://postgresql.org/",
             "tags": ["sql", "database", "relational"]},
            {"title": "VS Code Editor", "url": "https://code.visualstudio.com/",
             "tags": ["ide", "editor", "development"]},
            {"title": "Git Version Control System", "url": "https://git-scm.com/",
             "tags": ["version-control", "collaboration", "source-code"]},
            {"title": "GitHub Code Repository Hosting", "url": "https://github.com/",
             "tags": ["git", "collaboration", "open-source"]},
            {"title": "Stack Overflow Developer Community", "url": "https://stackoverflow.com/",
             "tags": ["community", "questions", "help"]},
            {"title": "FreeCodeCamp Learning Platform", "url": "https://freecodecamp.org/",
             "tags": ["free", "interactive", "certificates"]},
            {"title": "The Odin Project Curriculum", "url": "https://theodinproject.com/",
             "tags": ["full-stack", "project-based", "free"]},
            {"title": "Codecademy Interactive Courses", "url": "https://codecademy.com/",
             "tags": ["interactive", "hands-on", "structured"]},
            {"title": "CSS-Tricks Web Design Blog", "url": "https://css-tricks.com/",
             "tags": ["css", "frontend", "tutorials"]},
            {"title": "JavaScript.info Modern Tutorial", "url": "https://javascript.info/",
             "tags": ["javascript", "comprehensive", "modern"]},
            {"title": "Can I Use Browser Compatibility", "url": "https://caniuse.com/",
             "tags": ["browser-support", "compatibility", "features"]},
            {"title": "Bootstrap CSS Framework", "url": "https://getbootstrap.com/",
             "tags": ["css-framework", "responsive", "components"]},
            {"title": "Tailwind CSS Utility Framework", "url": "https://tailwindcss.com/",
             "tags": ["utility-first", "css", "responsive"]},
            {"title": "Vue.js Progressive Framework", "url": "https://vuejs.org/",
             "tags": ["frontend", "progressive", "reactive"]},
            {"title": "Angular Web Framework", "url": "https://angular.io/",
             "tags": ["typescript", "enterprise", "full-featured"]},
            {"title": "Webpack Module Bundler", "url": "https://webpack.js.org/",
             "tags": ["bundling", "build-tools", "optimization"]},
            {"title": "Vite Build Tool", "url": "https://vitejs.dev/", "tags": ["fast", "build-tool", "development"]},
            {"title": "Netlify Deployment Platform", "url": "https://netlify.com/",
             "tags": ["deployment", "jamstack", "hosting"]},
            {"title": "Vercel Deployment Platform", "url": "https://vercel.com/",
             "tags": ["nextjs", "deployment", "serverless"]},
            {"title": "Heroku Cloud Platform", "url": "https://heroku.com/", "tags": ["paas", "deployment", "backend"]},
            {"title": "AWS Web Services", "url": "https://aws.amazon.com/",
             "tags": ["cloud", "scalable", "enterprise"]},
            {"title": "Firebase Google Platform", "url": "https://firebase.google.com/",
             "tags": ["backend-as-service", "realtime", "authentication"]},
            {"title": "Postman API Testing", "url": "https://postman.com/",
             "tags": ["api-testing", "development", "collaboration"]},
            {"title": "Chrome DevTools", "url": "https://developers.google.com/web/tools/chrome-devtools",
             "tags": ["debugging", "performance", "browser-tools"]},
            {"title": "Web.dev Google Developers", "url": "https://web.dev/",
             "tags": ["performance", "best-practices", "modern-web"]}
        ]
    },
    "Blockchain": {
        "description": """Comprehensive blockchain and cryptocurrency course covering distributed ledger technology, 
        cryptographic principles, consensus mechanisms, smart contracts, DeFi protocols, NFTs, Web3 development, 
        Ethereum, Solidity programming, Bitcoin protocol, blockchain security, and practical application development. 
        Students will build decentralized applications and understand the economic and technical aspects of blockchain systems.""",
        "tasks": [
            "Implement a basic blockchain from scratch using Python",
            "Create a simple cryptocurrency with mining functionality",
            "Develop a smart contract for token creation on Ethereum",
            "Build a decentralized voting system using Solidity",
            "Create a NFT marketplace with minting and trading features",
            "Implement a decentralized finance (DeFi) lending protocol",
            "Build a cryptocurrency wallet with transaction capabilities",
            "Develop a supply chain tracking system on blockchain",
            "Create a decentralized autonomous organization (DAO) contract",
            "Implement a multi-signature wallet contract",
            "Build a decentralized exchange (DEX) with AMM functionality",
            "Create a blockchain-based identity verification system",
            "Develop a crowd-funding platform using smart contracts",
            "Implement a cross-chain bridge for token transfers",
            "Build a decentralized storage solution using IPFS",
            "Create a blockchain-based prediction market",
            "Develop a yield farming protocol with liquidity mining",
            "Implement a flash loan arbitrage strategy",
            "Build a decentralized insurance protocol",
            "Create a blockchain-based carbon credit marketplace",
            "Develop a Web3 social media platform",
            "Implement a decentralized domain name system",
            "Build a blockchain-based gaming platform with NFTs",
            "Create a algorithmic stablecoin mechanism",
            "Develop a layer 2 scaling solution",
            "Implement a zero-knowledge proof system",
            "Build a decentralized file sharing network",
            "Create a blockchain-based supply chain verification",
            "Develop a cross-border payment system using blockchain",
            "Implement a consensus mechanism simulation"
        ],
        "resources": [
            {"title": "Ethereum Official Documentation", "url": "https://ethereum.org/",
             "tags": ["ethereum", "smart-contracts", "web3"]},
            {"title": "Solidity Programming Language", "url": "https://soliditylang.org/",
             "tags": ["solidity", "smart-contracts", "ethereum"]},
            {"title": "Web3.js JavaScript Library", "url": "https://web3js.readthedocs.io/",
             "tags": ["web3", "javascript", "ethereum"]},
            {"title": "Truffle Development Framework", "url": "https://trufflesuite.com/",
             "tags": ["development", "testing", "deployment"]},
            {"title": "Hardhat Ethereum Development", "url": "https://hardhat.org/",
             "tags": ["development", "testing", "typescript"]},
            {"title": "OpenZeppelin Smart Contract Library", "url": "https://openzeppelin.com/",
             "tags": ["security", "standards", "contracts"]},
            {"title": "Remix IDE for Solidity", "url": "https://remix.ethereum.org/",
             "tags": ["ide", "browser-based", "development"]},
            {"title": "MetaMask Ethereum Wallet", "url": "https://metamask.io/",
             "tags": ["wallet", "browser-extension", "web3"]},
            {"title": "Chainlink Decentralized Oracles", "url": "https://chain.link/",
             "tags": ["oracles", "data-feeds", "defi"]},
            {"title": "IPFS Distributed Storage", "url": "https://ipfs.io/",
             "tags": ["storage", "distributed", "decentralized"]},
            {"title": "Bitcoin White Paper", "url": "https://bitcoin.org/bitcoin.pdf",
             "tags": ["bitcoin", "whitepaper", "satoshi"]},
            {"title": "Ethereum Yellow Paper", "url": "https://ethereum.github.io/yellowpaper/",
             "tags": ["ethereum", "technical", "specification"]},
            {"title": "CoinDesk Blockchain News", "url": "https://coindesk.com/",
             "tags": ["news", "industry", "analysis"]},
            {"title": "CoinGecko Market Data", "url": "https://coingecko.com/",
             "tags": ["market-data", "prices", "analytics"]},
            {"title": "DeFiPulse Protocol Analytics", "url": "https://defipulse.com/",
             "tags": ["defi", "tvl", "protocols"]},
            {"title": "Etherscan Ethereum Explorer", "url": "https://etherscan.io/",
             "tags": ["explorer", "transactions", "contracts"]},
            {"title": "Polygon Layer 2 Solution", "url": "https://polygon.technology/",
             "tags": ["layer2", "scaling", "ethereum"]},
            {"title": "Binance Smart Chain", "url": "https://bsc.binance.org/",
             "tags": ["bsc", "smart-contracts", "binance"]},
            {"title": "Avalanche Blockchain Platform", "url": "https://avax.network/",
             "tags": ["avalanche", "consensus", "subnets"]},
            {"title": "Solana High Performance Blockchain", "url": "https://solana.com/",
             "tags": ["solana", "performance", "rust"]},
            {"title": "Polkadot Interoperability", "url": "https://polkadot.network/",
             "tags": ["polkadot", "interoperability", "parachains"]},
            {"title": "Cardano Research Blockchain", "url": "https://cardano.org/",
             "tags": ["cardano", "research", "peer-review"]},
            {"title": "Hyperledger Enterprise Blockchain", "url": "https://hyperledger.org/",
             "tags": ["enterprise", "permissioned", "fabric"]},
            {"title": "ConsenSys Blockchain Company", "url": "https://consensys.net/",
             "tags": ["ethereum", "enterprise", "tools"]},
            {"title": "Binance Academy Educational Content", "url": "https://academy.binance.com/",
             "tags": ["education", "basics", "advanced"]},
            {"title": "Coursera Blockchain Courses", "url": "https://coursera.org/",
             "tags": ["courses", "university", "certificates"]},
            {"title": "edX Blockchain Programs", "url": "https://edx.org/", "tags": ["mit", "berkeley", "academic"]},
            {"title": "Blockchain Council Certifications", "url": "https://blockchain-council.org/",
             "tags": ["certification", "professional", "training"]},
            {"title": "CryptoZombies Learn Solidity", "url": "https://cryptozombies.io/",
             "tags": ["gamified", "solidity", "interactive"]},
            {"title": "Buildspace Web3 Projects", "url": "https://buildspace.so/",
             "tags": ["projects", "community", "web3"]},
            {"title": "Alchemy Blockchain Developer Platform", "url": "https://alchemy.com/",
             "tags": ["infrastructure", "apis", "development"]}
        ]
    }
}


def create_courses():
    """Create the 5 main courses."""
    print("🎓 Creating courses...")
    course_ids = {}

    for course_name, course_data in COURSES_DATA.items():
        print(f"Creating course: {course_name}")

        # Generate embedding for course description
        embedding = embed_text(f"{course_name} {course_data['description']}")

        course_record = {
            "title": course_name,
            "description": course_data["description"],
            "embedding": embedding
        }

        result = safe_insert("courses", course_record)
        if result:
            course_ids[course_name] = result["id"]
            print(f"✅ Created course: {course_name} (ID: {result['id']})")
        else:
            print(f"❌ Failed to create course: {course_name}")

        # Small delay to avoid rate limiting
        time.sleep(0.1)

    return course_ids


def create_tasks(course_ids):
    """Create tasks for each course."""
    print("\n📝 Creating tasks...")

    for course_name, course_id in course_ids.items():
        print(f"Creating tasks for {course_name}...")

        tasks_data = COURSES_DATA[course_name]["tasks"]

        for i, task_content in enumerate(tqdm(tasks_data, desc=f"Tasks for {course_name}")):
            task_title = f"Task {i + 1}: {task_content.split()[0:5]}"  # First 5 words as title
            task_title = " ".join(task_title[1:])  # Remove "Task X:"

            # Generate embedding for task
            embedding = embed_text(f"{task_title} {task_content}")

            task_record = {
                "title": task_title,
                "content": task_content,
                "course_id": course_id,
                "embedding": embedding
            }

            result = safe_insert("tasks", task_record)
            if not result:
                print(f"❌ Failed to create task: {task_title}")

            # Small delay every 10 tasks
            if i % 10 == 0:
                time.sleep(0.1)


def create_resources(course_ids):
    """Create resources for each course."""
    print("\n📚 Creating resources...")

    for course_name, course_id in course_ids.items():
        print(f"Creating resources for {course_name}...")

        resources_data = COURSES_DATA[course_name]["resources"]

        for i, resource_data in enumerate(tqdm(resources_data, desc=f"Resources for {course_name}")):
            # Generate embedding for resource
            text_for_embedding = f"{resource_data['title']} {' '.join(resource_data['tags'])}"
            embedding = embed_text(text_for_embedding)

            resource_record = {
                "title": resource_data["title"],
                "url": resource_data["url"],
                "tags": resource_data["tags"],
                "course_id": course_id,
                "embedding": embedding
            }

            result = safe_insert("resources", resource_record)
            if not result:
                print(f"❌ Failed to create resource: {resource_data['title']}")

            # Small delay every 10 resources
            if i % 10 == 0:
                time.sleep(0.1)


def verify_data():
    """Verify that data was inserted correctly."""
    print("\n🔍 Verifying inserted data...")

    tables = ['courses', 'tasks', 'resources']

    for table in tables:
        try:
            result = supabase.table(table).select("id", count="exact").execute()
            count = result.count
            print(f"✅ {table}: {count} records")

            # Get a sample record
            sample = supabase.table(table).select("*").limit(1).execute()
            if sample.data:
                print(f"   Sample: {sample.data[0].get('title', 'No title')}")
        except Exception as e:
            print(f"❌ Error checking {table}: {e}")


def main():
    """Main function to create all dummy data."""
    print("🚀 Starting comprehensive dummy data creation...")
    print("=" * 60)

    try:
        # Create courses first
        course_ids = create_courses()

        if not course_ids:
            print("❌ No courses created. Exiting...")
            return

        # Create tasks for each course
        create_tasks(course_ids)

        # Create resources for each course
        create_resources(course_ids)

        # Verify the data
        verify_data()

        print("\n" + "=" * 60)
        print("✅ Dummy data creation completed successfully!")
        print(f"📊 Created:")
        print(f"   - {len(course_ids)} courses")
        print(f"   - ~{len(course_ids) * 30} tasks (30 per course)")
        print(f"   - ~{len(course_ids) * 30} resources (30 per course)")

    except Exception as e:
        print(f"❌ Error during data creation: {e}")


if __name__ == "__main__":
    main()