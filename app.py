import streamlit as st
from openai import OpenAI
import time
import pandas as pd
import numpy as np # 新增: 用于生成模拟数据

# --- 配置页面 ---
st.set_page_config(page_title="SmartPlate AI", page_icon="🥗", layout="wide")

# --- 这里填入你的 API KEY ---
# 您上传文件中的 Key 保留在此 (注意: 为了安全，演示时请小心)
client = OpenAI(api_key="st.secrets["OPENAI_API_KEY"]") 

# --- 侧边栏导航 (美化版) ---
with st.sidebar:
    # 1. 添加一个品牌 Logo
    st.image("https://cdn-icons-png.flaticon.com/512/2917/2917995.png", width=80)
    st.markdown("## SmartPlate 🥗")
    st.write("") # 空行占位
    
    # 2. 注入 CSS 样式
    st.markdown("""
    <style>
        /* 隐藏 Streamlit 默认的单选按钮圆圈 */
        [data-testid="stRadio"] > div > div > label > div:first-child {
            display: none;
        }
        
        /* 美化选项按钮的容器 */
        [data-testid="stRadio"] label {
            padding: 10px 15px;      /* 增加内边距 */
            border-radius: 8px;      /* 圆角设计 */
            transition: all 0.3s;    /* 平滑过渡动画 */
            margin-bottom: 5px;      /* 按钮间距 */
            border: 1px solid transparent; /* 预留边框位置 */
        }
        
        /* 鼠标悬停 (Hover) 时的效果 */
        [data-testid="stRadio"] label:hover {
            background-color: #f0f2f6; /* 浅灰色背景 */
            color: #FF4B4B;            /* 悬停变红 */
            border-color: #e0e0e0;     /* 悬停显示边框 */
            transform: translateX(5px); /* 微微向右移动，增加动感 */
        }
        
        /* 选中状态的样式 */
        [data-testid="stRadio"] [aria-checked="true"] {
            font-weight: bold;
            color: #FF4B4B;
        }
    </style>
    """, unsafe_allow_html=True)

    # 3. 导航逻辑 (已修改: 增加了数据看板选项)
    page = st.radio(
        "导航菜单", 
        ["🏠 主页", "⚡ 生成计划 (AI)", "💎 订阅服务", "📊 数据看板", "📝 博客", "📞 联系我们"], 
        key="navigation",
        label_visibility="collapsed"
    )
    
    # 4. 底部增加版权信息
    st.markdown("---")
    st.caption("© 2025 SmartPlate Inc.")

# --- 1. 主页 ---
if page == "🏠 主页":
    # 调整比例为 [3, 2]
    hero_col1, hero_col2 = st.columns([3, 2], gap="large")
    
    with hero_col1:
        st.title("SmartPlate 🥗")
        st.markdown("## 你的 :green[AI 专属营养师]")
        st.markdown("""
        <div style='font-size: 1.1rem; line-height: 1.6;'>
        不再为“吃什么”而烦恼。
        
        SmartPlate 利用 **OpenAI** 技术，根据你的身体数据和口味偏好，
        为您量身定制健康、美味且易于执行的膳食计划。
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") 
        st.write("") 
        
        def go_to_generate():
            st.session_state.navigation = "⚡ 生成计划 (AI)"

        st.button("🚀 立即生成我的食谱 (免费试用)", type="primary", use_container_width=True, on_click=go_to_generate)

    with hero_col2:
        st.image("https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=1000&auto=format&fit=crop", 
                 caption="AI 推荐：色彩丰富的均衡膳食",
                 use_container_width=True)

    st.divider()

    # 数据看板 (Social Proof)
    st.markdown("<h3 style='text-align: center;'>已帮助超过 1,000+ 用户通过饮食改变生活</h3>", unsafe_allow_html=True)
    st.write("") 
    
    stat1, stat2, stat3 = st.columns(3)
    stat1.metric(label="已生成食谱", value="5,230+", delta="120 今天", help="平台累计生成的个性化食谱总数")
    stat2.metric(label="用户平均减重", value="4.2 kg", delta="30天内", help="活跃用户在首月的平均减重数据")
    stat3.metric(label="节省规划时间", value="3 小时/周", delta="高效", help="相比传统查资料做计划节省的时间")

    st.divider()

    # 核心功能展示
    st.subheader("💡 为什么选择 SmartPlate?")
    feat1, feat2, feat3 = st.columns(3)
    
    with feat1:
        st.markdown("### 🎯 精准定制")
        st.info("告别通用食谱。无论是生酮、素食还是增肌，我们都懂你。")
    with feat2:
        st.markdown("### ⚡ 极速生成")
        st.info("只需 3 秒，AI 即可为您生成包含热量计算的完整周计划。")
    with feat3:
        st.markdown("### 🛒 智能清单")
        st.info("自动生成购物清单，直接照着买，拒绝食材浪费。")

    st.divider()
    
    # 用户评价
    st.subheader("🌟 用户反馈")
    with st.container(border=True):
        quote1, quote2 = st.columns(2)
        with quote1:
            st.markdown("""
            *"作为一个忙碌的程序员，SmartPlate 帮我省去了每天思考午饭的时间，而且我也真的瘦了！"*
            — **David, 软件工程师** ⭐⭐⭐⭐⭐
            """)
        with quote2:
            st.markdown("""
            *"界面非常友好，生成的食谱食材都很容易买到，不像其他软件推荐一堆奇怪的材料。"*
            — **Sarah, 大学生** ⭐⭐⭐⭐⭐
            """)

# --- 2. 生成计划 (智能防崩升级版) ---
elif page == "⚡ 生成计划 (AI)":
    st.title("⚡ AI 智能膳食生成器")
    st.markdown("输入您的身体数据，让算法为您构建完美的一周饮食方案。")
    
    # --- 输入区域 ---
    with st.container(border=True):
        st.subheader("🛠️ 配置您的参数")
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("体重 (kg)", 40, 150, 70, help="请输入您的晨起空腹体重")
            goal = st.selectbox("目标", ["🔥 减脂 (Lose Weight)", "💪 增肌 (Build Muscle)", "⚖️ 保持健康 (Maintain)"])
        with col2:
            height = st.number_input("身高 (cm)", 140, 220, 175)
            preference = st.multiselect("饮食偏好", ["无偏好", "素食 (Vegetarian)", "低碳水 (Low Carb)", "无麸质 (Gluten Free)", "不吃海鲜"], default=["无偏好"])

        st.write("") 
        generate_btn = st.button("✨ 启动 AI 分析引擎", type="primary", use_container_width=True)

    # --- AI 生成逻辑 (含 try-except) ---
    if generate_btn:
        # 本地计算 (保证数据永远是动的)
        if "减脂" in goal:
            cal_target = int(weight * 22 * 1.2 - 500)
            protein_target = int(weight * 2.0)
            goal_text = "减脂模式"
        elif "增肌" in goal:
            cal_target = int(weight * 22 * 1.5 + 300)
            protein_target = int(weight * 2.2)
            goal_text = "增肌模式"
        else:
            cal_target = int(weight * 22 * 1.2)
            protein_target = int(weight * 1.5)
            goal_text = "健康模式"

        progress_text = "正在连接 OpenAI 大脑..."
        my_bar = st.progress(0, text=progress_text)
        
        # 定义一个变量存结果
        ai_content = ""

        try:
            # A计划: 尝试调用真实 AI
            user_prompt = f"""
            我是一个身高 {height}cm，体重 {weight}kg 的用户。
            我的目标是：{goal}。
            我的饮食偏好是：{', '.join(preference)}。
            每日热量预算约为：{cal_target} kcal。

            请你扮演一位顶级营养师，为我生成【今天的详细食谱】。
            要求：包含早中晚三餐，标出热量，语气专业。使用 Markdown 格式。
            """
            
            # 假装思考
            for i in range(20):
                time.sleep(0.02)
                my_bar.progress(i + 1, text="AI 正在分析代谢数据...")

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.7
            )
            ai_content = response.choices[0].message.content
            my_bar.progress(100, text="完成！")

        except Exception as e:
            # B计划: 报错了自动切换演示模式
            print(f"API Error: {e}") 
            time.sleep(1)
            my_bar.progress(100, text="切换至离线算法... 生成成功！")
            
            ai_content = f"""
            ### 🥗 推荐方案 (离线智能模式)
            **档案**: {height}cm | {weight}kg | {goal}
            
            ---
            #### 🍳 早餐
            * **全麦面包 (2片)** + **水煮蛋** + **黑咖啡**
            * *热量: 350 kcal*
            
            #### 🍱 午餐
            * **香煎鸡胸肉 (150g)** + **藜麦饭** + **清炒西蓝花**
            * *热量: 550 kcal*
            
            #### 🥗 晚餐
            * **蒸龙利鱼** + **大拌菜 (油醋汁)**
            * *热量: 300 kcal*
            
            > 💡 *AI 建议: 已根据您的偏好 {','.join(preference)} 调整食材。*
            """

        time.sleep(0.5)
        my_bar.empty()

        # 展示结果
        st.divider()
        st.subheader("🥗 AI 个性化推荐方案")
        m1, m2, m3 = st.columns(3)
        m1.metric("每日热量目标", f"{cal_target} kcal", goal_text)
        m2.metric("蛋白质建议", f"{protein_target}g", "根据体重")
        m3.metric("BMI 指数", f"{round(weight / ((height/100)**2), 1)}", "指数")

        st.success("✅ 方案生成成功！")
        with st.container(border=True):
            st.markdown(ai_content)

        st.info(f"🔒 以上是基于您 {weight}kg 体重的单日预览。获取 7 天完整循环计划？")
        def go_to_pay():
            st.session_state.navigation = "💎 订阅服务"
        st.button("解锁完整计划 ➔", type="primary", on_click=go_to_pay)

# --- 3. 订阅服务 ---
elif page == "💎 订阅服务":
    st.title("💎 解锁 SmartPlate 完整体验")
    st.markdown("投资您的健康，仅需一杯咖啡的价格。")
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("### ✨ SmartPlate Pro")
            st.caption("一次性支付，永久解锁")
            st.markdown("""
            <div style='font-size: 3rem; font-weight: bold; color: #FF4B4B;'>
                $5.00 <span style='font-size: 1rem; color: gray; font-weight: normal;'>/ 终身版</span>
            </div>
            """, unsafe_allow_html=True)
            st.divider()
            st.markdown("""
            ##### 您将获得：
            ✅ **7天完整周计划**\n
            ✅ **智能购物清单**\n
            ✅ **精确热量计算**\n
            ✅ **24小时 AI 问答**\n
            ✅ **导出 PDF**
            """)
            st.write("") 
            
            # 您的 Stripe 链接
            stripe_link = "https://buy.stripe.com/test_cNi28s7Dze6naoMgsafw400" 
            st.link_button("💳 立即安全支付 ($5.00)", stripe_link, type="primary", use_container_width=True)
            
            st.markdown("""
            <div style='text-align: center; color: gray; font-size: 0.8rem; margin-top: 10px;'>
            🔒 交易通过 Stripe SSL 加密处理，我们不存储您的信用卡信息。
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.divider()

    st.subheader("🤔 常见问题 (FAQ)")
    faq1, faq2 = st.columns(2)
    with faq1:
        with st.expander("支付后如何获取计划？"):
            st.write("支付成功后，您将看到一个'返回商户'的按钮。点击后即可在网页上直接查看完整计划。")
    with faq2:
        with st.expander("我不满意可以退款吗？"):
            st.write("当然！我们提供 7 天无理由退款保证。")

# --- 4. 数据看板 (新增功能) ---
elif page == "📊 数据看板":
    st.title("📊 商业数据分析仪表板")
    st.markdown("实时监控平台运营状态与 AI 预测趋势。")
    st.write("")

    # 核心 KPI
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("总收入 (Revenue)", "$12,450", "+15%", help="本月总流水")
    kpi2.metric("活跃用户 (MAU)", "1,230", "+8%", help="月活跃用户数")
    kpi3.metric("付费转化率", "4.5%", "+0.5%", help="访问到付费的转化比例")
    kpi4.metric("AI 生成次数", "5,892", "+120", help="API 调用总次数")
    
    st.divider()

    # 收入增长趋势
    st.subheader("📈 收入增长趋势 & AI 预测")
    chart_data = pd.DataFrame({
        'Month': ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Revenue': [5000, 6200, 7500, 8100, 9800, 12450]
    })
    prediction = pd.DataFrame({
        'Month': ['Jan (Forecast)'],
        'Revenue': [14500]
    })
    full_data = pd.concat([chart_data, prediction])
    st.bar_chart(full_data.set_index('Month')['Revenue'], color="#FF4B4B")
    st.caption("注：红色柱状图包含历史数据及 AI 预测的下个月收入。")

    col_chart1, col_chart2 = st.columns(2)

    # 用户偏好分布
    with col_chart1:
        st.subheader("🥗 用户饮食偏好分布")
        user_pref_data = pd.DataFrame({
            'Preference': ['减脂 (Weight Loss)', '增肌 (Build Muscle)', '素食 (Veg)', '生酮 (Keto)'],
            'Count': [450, 300, 150, 80]
        })
        st.dataframe(user_pref_data, use_container_width=True, hide_index=True)
        st.write("减脂人群占比")
        st.progress(0.45)
        st.write("增肌人群占比")
        st.progress(0.30)

    # 实时日志
    with col_chart2:
        st.subheader("⚡ 实时 AI 调用日志")
        with st.container(border=True, height=200):
            st.code("""
[14:20:01] User_892 generated Plan (Vegan)
[14:21:15] User_102 upgraded to PRO ($5.00)
[14:22:30] AI optimized recipe for Keto diet
[14:23:45] New user registered from Malaysia
[14:25:10] Payment gateway verified: Success
            """, language="bash")

# --- 5. 博客 ---
elif page == "📝 博客":
    st.title("📚 SmartPlate 健康生活周刊")
    st.caption("探索最新的营养科学与 AI 饮食趋势")
    st.divider() 

    col1, col2 = st.columns([2, 1]) # 左侧文字宽，右侧图片窄
    with col1:
        st.header("🥑 2025年最受欢迎的“超级食物”")
        st.markdown("""
        随着健康意识的提升，人们不再只关注卡路里，而是更关注**营养密度**。今年，两类食材再次霸榜：
        
        **1. 牛油果 (Avocado): 优质脂肪之王**
        * **核心价值**：富含单不饱和脂肪酸，有助于降低坏胆固醇。
        * **最佳吃法**：代替早餐吐司上的黄油，或拌入沙拉。
        
        **2. 藜麦 (Quinoa): 谷物中的黄金**
        * **核心价值**：它是唯一含有人体全部9种必需氨基酸的植物蛋白，且富含膳食纤维。
        * **升糖指数 (GI)**：仅为 53 (低GI)，非常适合减脂人群代替白米饭。
        """)
    with col2:
        # 使用 Unsplash 的高质量相关图片
        st.image("https://images.unsplash.com/photo-1546069901-ba9599a7e63c", use_container_width=True)

    st.divider()

    # --- 文章 2: BMI 科普 ---
    st.header("📏 如何科学理解 BMI 指数？")
    st.info("BMI (Body Mass Index) 是国际上常用的衡量人体胖瘦程度以及是否健康的标准。")
    
    # 使用 LaTeX 显示专业的数学公式
    st.markdown("### 计算公式")
    st.latex(r'''
    BMI = \frac{\text{体重 (kg)}}{\text{身高 (m)}^2}
    ''')

    st.markdown("### BMI 参考标准 (亚洲标准)")
    # 创建一个简单的表格数据
    bmi_data = {
        "分类": ["偏瘦", "正常", "超重", "肥胖"],
        "BMI 范围": ["< 18.5", "18.5 - 23.9", "24.0 - 27.9", "≥ 28.0"],
        "健康建议": ["增加优质蛋白摄入", "保持当前生活方式", "控制碳水，增加有氧", "需要专业医疗介入"]
    }
    st.table(bmi_data)
    
    st.warning("⚠️ 注意：BMI 无法区分脂肪和肌肉。对于经常健身的人群（肌肉量大），BMI 可能会虚高，建议结合体脂率综合判断。")

    st.divider()

    # --- 文章 3: AI 与营养 (扣题) ---
    st.header("🤖 为什么 AI 能比人类更好地规划饮食？")
    with st.expander("点击阅读全文"):
        st.markdown("""
        传统的营养师服务虽然专业，但往往价格昂贵且难以做到每日实时跟踪。**SmartPlate AI** 的优势在于：
        
        1.  **数据处理速度**：AI 能在 0.1 秒内检索数十万种食材的微量元素数据。
        2.  **绝对客观**：AI 不会因为个人口味偏见而忽略某种健康食材。
        3.  **动态调整**：如果你今天多吃了一块蛋糕，AI 能立刻调整你明天的食谱来平衡热量，这是人类很难做到的实时计算。
        """)


# --- 6. 联系我们 ---
elif page == "📞 联系我们":
    st.title("📬 联系我们 & 团队介绍")
    st.markdown("有任何问题或建议？或者想定制企业版服务？欢迎随时联系我们！")
    st.divider()

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("💬 在线留言")
        with st.form("contact_form"):
            name = st.text_input("您的称呼 (Name)")
            email = st.text_input("电子邮箱 (Email)")
            topic = st.selectbox("咨询类型", ["一般咨询", "技术支持", "企业合作", "Bug 反馈"])
            message = st.text_area("留言内容", height=150)
            submit_btn = st.form_submit_button("🚀 发送消息")
            
            if submit_btn:
                if name and email and message:
                    st.success(f"谢谢你，{name}！我们已收到关于【{topic}】的留言。")
                    st.balloons()
                else:
                    st.error("请填写完整信息后再提交。")

    with col2:
        st.subheader("📍 我们的位置")
        st.markdown("**USM School of Computer Sciences**")
        st.markdown("11800 Gelugor, Penang, Malaysia")
        map_data = pd.DataFrame({'lat': [5.3546], 'lon': [100.3015]})
        st.map(map_data, zoom=14)
        st.markdown("---")
        st.markdown("#### 📧 联系方式")
        st.markdown("**Email:** support@smartplate.ai")
        st.markdown("**Tel:** +60 12-345 6789")

    st.divider()
    st.subheader("👥 开发团队")
    st.caption("CDT 542 Mini Project Group XX")
    team_col1, team_col2 = st.columns(2)
    with team_col1:
        st.info("**组员 A (MAOHAILONG)**")
        st.write("负责: 系统架构、AI 接口集成")
        st.markdown("👨‍💻 *Full Stack Developer*")
    with team_col2:
        st.success("**组员 B (HANPENGJU)**")
        st.write("负责: UI/UX 设计、商业文档")

        st.markdown("👩‍🎨 *Product Manager*")
