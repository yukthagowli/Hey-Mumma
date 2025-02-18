"""
Module for fetal development information and tracking
"""
import os
from pathlib import Path

def get_placeholder_html(week):
    """
    Returns HTML for a placeholder image with week information
    """
    return f"""
        <div style="
            width: 100%;
            height: 400px;
            background-color: #f0f2f6;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            margin: 10px 0;
            flex-direction: column;
            text-align: center;
            padding: 20px;
            box-sizing: border-box;
        ">
            <div style="
                font-size: 24px;
                color: #262730;
                margin-bottom: 10px;
            ">
                Fetal Development
            </div>
            <div style="
                font-size: 20px;
                color: #262730;
            ">
                Week {week}
            </div>
        </div>
    """

def get_image_path(week):
    """
    Returns the path to the fetal development image for the specified week
    """
    try:
        base_path = Path(__file__).parent.parent / "graphics" / "fetal_development"
        image_path = base_path / f"week_{week}.jpg"
        
        # Return actual image path if it exists, otherwise return None
        if image_path.exists():
            return str(image_path)
        return None
    except Exception:
        return None

def get_size_comparison(week):
    """
    Returns a familiar object to compare the baby's size to for the given week
    """
    size_comparisons = {
        4: "poppy seed",
        5: "sesame seed",
        6: "lentil",
        7: "blueberry",
        8: "raspberry",
        9: "grape",
        10: "kumquat",
        11: "fig",
        12: "lime",
        13: "lemon",
        14: "orange",
        15: "apple",
        16: "avocado",
        17: "pomegranate",
        18: "sweet potato",
        19: "mango",
        20: "banana",
        21: "carrot",
        22: "coconut",
        23: "grapefruit",
        24: "corn",
        25: "cauliflower",
        26: "lettuce head",
        27: "rutabaga",
        28: "eggplant",
        29: "butternut squash",
        30: "cabbage",
        31: "coconut",
        32: "jicama",
        33: "pineapple",
        34: "cantaloupe",
        35: "honeydew melon",
        36: "romaine lettuce",
        37: "swiss chard",
        38: "leek",
        39: "watermelon",
        40: "small pumpkin"
    }
    return size_comparisons.get(week, "size varies")

def get_fetal_development_info(week):
    """
    Returns detailed information about fetal development for a specific week
    """
    development_info = {
        1: {
            "title": "Week 1: Preparing for Conception",
            "size": "Not visible yet",
            "size_comparison": "N/A",
            "weight": "N/A",
            "highlights": [
                "Your body is preparing for possible conception",
                "Egg is maturing in the ovary",
                "Uterine lining is thickening"
            ],
            "details": "This is the week of your period, and your body is preparing for the possibility of conception. While there's no baby yet, your body is getting ready for the journey ahead.",
            "what_to_expect": [
                "Menstruation",
                "Hormonal changes",
                "Egg maturation"
            ],
            "tips": [
                "Take prenatal vitamins",
                "Maintain a healthy diet",
                "Track your cycle",
                "Avoid alcohol and smoking"
            ]
        },
        2: {
            "title": "Week 2: Conception Week",
            "size": "Too small to measure",
            "size_comparison": "N/A",
            "weight": "N/A",
            "highlights": [
                "Ovulation occurs",
                "Egg may be fertilized",
                "Journey through fallopian tube begins"
            ],
            "details": "During this week, ovulation occurs and if an egg is fertilized, your journey to parenthood begins. The fertilized egg starts its journey through the fallopian tube.",
            "what_to_expect": [
                "Ovulation",
                "Possible fertilization",
                "Hormonal changes"
            ],
            "tips": [
                "Take prenatal vitamins",
                "Maintain a healthy diet",
                "Track your cycle",
                "Avoid alcohol and smoking"
            ]
        },
        3: {
            "title": "Week 3: Implantation",
            "size": "0.1 mm",
            "size_comparison": "N/A",
            "weight": "N/A",
            "highlights": [
                "Fertilized egg implants in uterus",
                "Placenta begins to form",
                "Pregnancy hormone (hCG) production starts"
            ],
            "details": "The fertilized egg implants itself in your uterine wall. The placenta begins to form, and your body starts producing pregnancy hormones.",
            "what_to_expect": [
                "Implantation",
                "Hormonal changes",
                "Possible spotting"
            ],
            "tips": [
                "Take prenatal vitamins",
                "Maintain a healthy diet",
                "Track your cycle",
                "Avoid alcohol and smoking"
            ]
        },
        4: {
            "title": "Week 4: Early Development",
            "size": "0.4 mm",
            "size_comparison": get_size_comparison(4),
            "weight": "N/A",
            "highlights": [
                "Amniotic sac forms",
                "Basic structures begin to develop",
                "Positive pregnancy test possible"
            ],
            "details": "The amniotic sac forms around your growing embryo. Basic structures that will become the placenta and umbilical cord are developing.",
            "what_to_expect": [
                "Early development",
                "Hormonal changes",
                "Possible morning sickness"
            ],
            "tips": [
                "Take prenatal vitamins",
                "Maintain a healthy diet",
                "Track your cycle",
                "Avoid alcohol and smoking"
            ]
        },
        5: {
            "title": "Week 5: Heart Development",
            "size": "2 mm",
            "size_comparison": get_size_comparison(5),
            "weight": "N/A",
            "highlights": [
                "Heart begins to beat",
                "Neural tube forms",
                "Basic facial features begin to form"
            ],
            "details": "Your baby's heart begins to beat and the neural tube, which will become the brain and spinal cord, starts to develop.",
            "what_to_expect": [
                "Heart development",
                "Hormonal changes",
                "Possible morning sickness"
            ],
            "tips": [
                "Take prenatal vitamins",
                "Maintain a healthy diet",
                "Track your cycle",
                "Avoid alcohol and smoking"
            ]
        },
        6: {
            "title": "Week 6: Early Organ Development",
            "size": "6 mm",
            "size_comparison": get_size_comparison(6),
            "weight": "N/A",
            "highlights": [
                "Brain and head grow rapidly",
                "Arm and leg buds appear",
                "Heart beats 100-160 times per minute"
            ],
            "details": "The brain and head grow rapidly. Arm and leg buds begin to form, and the heart now beats around 100-160 times per minute.",
            "what_to_expect": [
                "Early organ development",
                "Hormonal changes",
                "Possible morning sickness"
            ],
            "tips": [
                "Take prenatal vitamins",
                "Maintain a healthy diet",
                "Track your cycle",
                "Avoid alcohol and smoking"
            ]
        },
        7: {
            "title": "Week 7: Continued Growth",
            "size": "13 mm",
            "size_comparison": get_size_comparison(7),
            "weight": "N/A",
            "highlights": [
                "Arms and legs growing longer",
                "Digestive system developing",
                "Face features becoming more defined"
            ],
            "details": "Your baby's arms and legs are growing longer, and small hands and feet are forming. The digestive system and major organs continue to develop.",
            "what_to_expect": [
                "Continued growth",
                "Hormonal changes",
                "Possible morning sickness"
            ],
            "tips": [
                "Take prenatal vitamins",
                "Maintain a healthy diet",
                "Track your cycle",
                "Avoid alcohol and smoking"
            ]
        },
        8: {
            "title": "Week 8: Major Development",
            "size": "16 mm",
            "size_comparison": get_size_comparison(8),
            "weight": "N/A",
            "highlights": [
                "All major organs formed",
                "Bones begin to form",
                "Movement begins (though not felt yet)"
            ],
            "details": "All major organs and structures have formed. Bones begin to form, and your baby starts making small movements, though you won't feel them yet.",
            "what_to_expect": [
                "Major development",
                "Hormonal changes",
                "Possible morning sickness"
            ],
            "tips": [
                "Take prenatal vitamins",
                "Maintain a healthy diet",
                "Track your cycle",
                "Avoid alcohol and smoking"
            ]
        },
        9: {
            "title": "Week 9: Fetus Stage Begins",
            "size": "23 mm",
            "size_comparison": get_size_comparison(9),
            "weight": "N/A",
            "highlights": [
                "Now called a fetus",
                "External genitals develop",
                "Fingers and toes are distinct"
            ],
            "details": "Your baby is now called a fetus. External genitals begin to form, and fingers and toes are more distinct.",
            "what_to_expect": [
                "Fetus stage begins",
                "Hormonal changes",
                "Possible morning sickness"
            ],
            "tips": [
                "Take prenatal vitamins",
                "Maintain a healthy diet",
                "Track your cycle",
                "Avoid alcohol and smoking"
            ]
        },
        10: {
            "title": "Week 10: Rapid Growth",
            "size": "31 mm",
            "size_comparison": get_size_comparison(10),
            "weight": "N/A",
            "highlights": [
                "Vital organs functioning",
                "Fingernails begin to form",
                "More defined facial features"
            ],
            "details": "All vital organs are now functioning. Fingernails begin to form, and facial features become more defined.",
            "what_to_expect": [
                "Rapid growth",
                "Hormonal changes",
                "Possible morning sickness"
            ],
            "tips": [
                "Take prenatal vitamins",
                "Maintain a healthy diet",
                "Track your cycle",
                "Avoid alcohol and smoking"
            ]
        },
        11: {
            "title": "Week 11: Growing and Developing",
            "size": "4.1 cm",
            "size_comparison": get_size_comparison(11),
            "weight": "7 grams",
            "highlights": [
                "Baby's head makes up about half of their length",
                "Tooth buds are forming",
                "Nail beds are developing",
                "External genitals are developing"
            ],
            "details": "Your baby is now officially a fetus! They're growing rapidly, with clear human features. The face is well-formed, and external genitals are beginning to show gender differences.",
            "what_to_expect": [
                "Morning sickness may be improving",
                "Increased energy levels",
                "Visible bump may start forming"
            ],
            "tips": [
                "Start pregnancy exercises if approved by doctor",
                "Continue prenatal vitamins",
                "Stay hydrated",
                "Plan for prenatal testing"
            ]
        },
        12: {
            "title": "Week 12: End of First Trimester",
            "size": "5.4 cm",
            "size_comparison": get_size_comparison(12),
            "weight": "14 grams",
            "highlights": [
                "Reflexes are developing",
                "Can make sucking movements",
                "Intestines move into abdomen",
                "Brain development accelerates"
            ],
            "details": "Your baby's systems are becoming more complex. They can now make sucking movements and their digestive system is beginning to practice contraction movements.",
            "what_to_expect": [
                "End of first trimester",
                "Reduced risk of miscarriage",
                "Increased appetite"
            ],
            "tips": [
                "Schedule second-trimester checkups",
                "Consider announcing pregnancy",
                "Continue healthy eating habits",
                "Start planning maternity leave"
            ]
        }
        # Continue with weeks 13-40...
    }
    
    # Add remaining weeks dynamically with basic information
    for i in range(13, 41):
        if i not in development_info:
            development_info[i] = {
                "title": f"Week {i}",
                "size": f"{i*2.5:.1f} cm (approximate)",
                "size_comparison": get_size_comparison(i),
                "weight": f"{max(7, (i-11)*28):.0f} grams (approximate)",
                "highlights": [
                    "Baby continues to grow and develop",
                    "Systems becoming more mature",
                    "Movement becoming stronger"
                ],
                "details": f"Week {i} marks continued growth and development of your baby. Their organs and systems are becoming more sophisticated.",
                "what_to_expect": [
                    "Regular prenatal checkups",
                    "Continued weight gain",
                    "Fetal movement (after week 16)"
                ],
                "tips": [
                    "Monitor fetal movements",
                    "Stay active as approved by doctor",
                    "Maintain healthy diet",
                    "Get adequate rest"
                ]
            }
    
    return development_info.get(week, {
        "title": f"Week {week}",
        "size": "Information being updated",
        "size_comparison": "N/A",
        "weight": "N/A",
        "highlights": ["Please check with your healthcare provider for detailed information"],
        "details": "Detailed information for this week is being updated.",
        "what_to_expect": ["Consult your healthcare provider"],
        "tips": ["Follow your doctor's advice"]
    })

def get_development_milestones():
    """
    Returns key development milestones throughout pregnancy
    """
    return {
        "First Trimester": [
            "Heart begins beating (Week 6-7)",
            "Brain and spinal cord form (Week 7)",
            "Limbs develop (Week 8)",
            "Basic facial features form (Week 9)",
            "External genitals begin forming (Week 11)",
            "Fingernails and toenails form (Week 12)"
        ],
        "Second Trimester": [
            "Gender can be determined (Week 16-20)",
            "Movement can be felt (Week 18-20)",
            "Fingerprints form (Week 20)",
            "Hair begins to grow (Week 22)",
            "Hearing develops (Week 23)",
            "Regular sleep cycles begin (Week 24)",
            "Lungs begin to develop (Week 26)"
        ],
        "Third Trimester": [
            "Eyes can open (Week 28)",
            "Brain grows rapidly (Week 29-32)",
            "Bones fully develop (Week 32-34)",
            "Lungs mature (Week 35-36)",
            "Baby drops into birth position (Week 36-38)",
            "Full term development (Week 39-40)"
        ]
    }

def get_weekly_exercises(week):
    """
    Returns recommended exercises for the specified week
    """
    if week <= 13:  # First trimester
        return [
            "Walking (20-30 minutes daily)",
            "Prenatal yoga (with instructor approval)",
            "Kegel exercises",
            "Light stretching"
        ]
    elif week <= 26:  # Second trimester
        return [
            "Swimming",
            "Stationary cycling",
            "Low-impact aerobics",
            "Prenatal yoga",
            "Walking (30 minutes daily)",
            "Kegel exercises"
        ]
    else:  # Third trimester
        return [
            "Walking (as tolerated)",
            "Swimming",
            "Prenatal yoga (modified)",
            "Pelvic tilts",
            "Kegel exercises",
            "Gentle stretching"
        ]

def get_nutrition_tips(week):
    """
    Returns nutrition recommendations for the specified week
    """
    general_tips = [
        "Take prenatal vitamins daily",
        "Stay hydrated (8-10 glasses of water)",
        "Eat plenty of fruits and vegetables",
        "Include protein-rich foods",
        "Choose whole grains"
    ]
    
    if week <= 13:
        return {
            "focus_nutrients": ["Folic acid", "Iron", "Vitamin B6"],
            "recommended_foods": [
                "Leafy greens",
                "Citrus fruits",
                "Lean meats",
                "Whole grains"
            ],
            "foods_to_avoid": [
                "Raw fish",
                "Unpasteurized dairy",
                "Raw eggs",
                "Excess caffeine"
            ],
            "tips": general_tips + [
                "Eat small, frequent meals to manage nausea",
                "Consider ginger for morning sickness"
            ]
        }
    elif week <= 26:
        return {
            "focus_nutrients": ["Calcium", "Vitamin D", "Omega-3"],
            "recommended_foods": [
                "Dairy products",
                "Fatty fish (cooked)",
                "Nuts and seeds",
                "Legumes"
            ],
            "foods_to_avoid": [
                "Raw fish",
                "Unpasteurized foods",
                "High-mercury fish"
            ],
            "tips": general_tips + [
                "Increase caloric intake by ~300 calories",
                "Focus on nutrient-dense foods"
            ]
        }
    else:
        return {
            "focus_nutrients": ["Iron", "Calcium", "Protein"],
            "recommended_foods": [
                "Iron-rich foods",
                "High-fiber foods",
                "Protein sources",
                "Complex carbohydrates"
            ],
            "foods_to_avoid": [
                "Raw fish",
                "Unpasteurized foods",
                "Excess sugar"
            ],
            "tips": general_tips + [
                "Eat smaller, more frequent meals",
                "Choose foods rich in fiber to prevent constipation"
            ]
        }
