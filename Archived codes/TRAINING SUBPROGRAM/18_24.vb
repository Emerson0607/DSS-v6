Sub Update_18_24()
    Dim lastRow As Long
    Dim i As Long
    
    ' Find the last row of data in column A
    lastRow = Cells(Rows.Count, "A").End(xlUp).Row
    
    ' Loop through each row
    For i = 1 To lastRow
        
        '########################### LITERACY #################################
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Literacy" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Digital Literacy Training"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Mobile Technology Libraries"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Virtual STEM Education Initiatives"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Cybersecurity Awareness Campaigns"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Virtual STEM Education Initiatives"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Cybersecurity Awareness Campaigns"
            End If
        End If

        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Literacy" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "ICT Skills Training"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Basic Computer Literacy Workshop"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Microsoft Office Training Sessions (Word, Excel, PowerPoint)"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Internet Skills and Online Safety Workshops"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Virtual STEM Education Initiatives"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Cybersecurity Awareness Campaigns"
            End If
        End If

        
        '########################### Socio-economic #################################
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Socio-economic" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Entrepreneurship Bootcamp"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Job Fairs and Career Counseling Sessions "
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Entrepreneurship Training"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Financial Literacy seminars"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Skills development workshops in trades"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Entrepreneurship Training"
            End If
        End If
        
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Socio-economic" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Livelihood Skills Training"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Job Fair and Skills Training Expo"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "ICT Skills Training"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Entrepreneurship Development Training"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Agribusiness Management Workshop"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Cybersecurity Awareness Campaigns"
            End If
        End If
        
        '########################### Environmental Stewardship #################################
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Environmental Stewardship" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Tree-Planting Campaign"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Upcycling Crafts Workshop"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "DIY Natural Cleaning Products Workshop"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Climate Change Awareness Seminar"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Water Conservation Seminar"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Biodiversity Conservation Awareness Campaigns"
            End If
        End If
        
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Environmental Stewardship" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Recycling and Waste Management Programs"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Clean-up Drives"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Sustainable Energy Workshops"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Climate Change Resilience Training"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Urban Gardening Project"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Tree-Planting Campaign"
            End If
        End If
        
        '########################### Health and Wellness #################################
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Health and Wellness" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Nutrition Basics Workshop"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Healthy Cooking Class"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Community Fitness Classes"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Holistic Health Seminar"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Work-Life Balance Workshop"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Stress Management Seminar"
            End If
        End If
        
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Health and Wellness" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Food Assistance Programs"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Community Health Fairs"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Holistic Health Seminar"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Emotional Wellness Seminar"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Stress Management Seminar"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Work-Life Balance Workshop"
            End If
        End If

        '########################### Cultural Enhancement #################################
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Cultural Enhancement" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Traditional Arts and Crafts Workshops"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Intercultural Dialogue Workshops"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Community Arts Festival"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Folk Dance and Music Performances"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Cultural festivals showcasing local traditions and heritage"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Historical site preservation and restoration efforts
"
            End If
        End If
        
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Cultural Enhancement" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Language revitalization program"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Community theater productions"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Oral history projects"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Historical Site Preservation Projects"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Intercultural Dialogue Workshops"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Community Arts Festival"
            End If
        End If
        
        '########################### Values Formation #################################
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Values Formation" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Values Education Curriculum"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Interfaith Dialogue Series"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Anti-bullying campaigns and peer support groups"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Building Self-Confidence and Values in Adolescence"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Self-Discovery Workshops"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Career Development and Values Alignment for Young Professionals
"
            End If
        End If
        
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Values Formation" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Basic Values Literacy Workshops"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Values Exploration"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Ethics seminars"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Cyberbullying Prevention Workshops"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Rediscovering Passion and Purpose Training"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Career Planning Workshops"
            End If
        End If
        
        '########################### Disaster Management #################################
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Disaster Management" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Climate Change Adaptation Workshop"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Disaster Risk Mapping"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Search and Rescue Training"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Disaster Recovery and Rehabilitation Program"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Disaster risk reduction education"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Psychological first aid trainin"
            End If
        End If
            
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Disaster Management" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "First Aid Training"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Flood/Earthquake/Fire Preparedness and Response Training"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Search and Rescue Simulation Exercise"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Hazard Identification and Risk Assessment Workshop"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Livestock and Agricultural Disaster Preparedness Training"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Water, Sanitation, and Hygiene (WASH) in Emergencies Training"
            End If
        End If
        
        '########################### Gender and Development #################################
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Gender and Development" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "First Aid Training"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Gender empowerment workshops focusing on leadership and entrepreneurship"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Gender sensitivity training"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Advocacy campaigns against gender-based violence"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Legal literacy seminars on gender rights and laws
"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Counseling and Mental Health Support"
            End If
        End If
        
        If Cells(i, 2).Value = "18-24" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Gender and Development" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Reproductive Health Seminar"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Gender-responsive Planning and Budgeting Advocacy"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Gender Concepts and Gender Analysis (GA) Tools Gender Sensitivity Training"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Pressure and Stress Management Seminar"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Mental Health Awareness Seminar"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Orientation and Anti-Sexual and Safe Spaces"
            End If
        End If
    Next i
End Sub




