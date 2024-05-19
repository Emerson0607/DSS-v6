Sub Update_25_34()
    Dim lastRow As Long
    Dim i As Long
    
    ' Find the last row of data in column A
    lastRow = Cells(Rows.Count, "A").End(xlUp).Row
    
    ' Loop through each row
    For i = 1 To lastRow
        '########################### LITERACY ################################# Masters Degree
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Literacy" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Digital Literacy Training"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Mobile Technology Libraries"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Virtual STEM Education Initiatives"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Cybersecurity Awareness Campaigns"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "ICT Skills Training"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Professional Development Seminars"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Internet Skills and Online Safety Workshops"
            End If
        End If
        
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Literacy" Then
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
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Cybersecurity Awareness Campaigns"
            End If
        End If
        
        '########################### Socio-economic #################################
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Socio-economic" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Entrepreneurship Bootcamp"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Microenterprise Development Fund"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Microfinance Programs"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Small Business Incubation Centers"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Skills development workshops in trades"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Entrepreneurship training"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Financial literacy seminars"
            End If
        End If
        
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Socio-economic" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Vocational Training Workshops"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Job Fair and Skills Training Expo"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Job Fairs and Career Counseling Sessions"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Entrepreneurship training"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Cooperative Development Initiatives"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Skills development workshops in trades"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Financial literacy seminars"
            End If
        End If
        
        '########################### Environmental Stewardship #################################
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Environmental Stewardship" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Tree-Planting Campaign"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Urban Gardening Project"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Environmental Education Workshops"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Recycling and Waste Management Programs"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Climate Change Resilience Training"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Sustainable Energy Workshops"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Urban Gardening Project"
            End If
        End If
        
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Environmental Stewardship" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Tree-Planting Campaign"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Environmental Education Workshops"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Biodiversity conservation awareness campaigns"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Sustainable agriculture practices workshops"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Climate Change Resilience Training"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Environmental Education Workshops"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Urban Gardening Project"
            End If
        End If
        
        '########################### Health and Wellness #################################
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Health and Wellness" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Nutrition Program"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Community Fitness Classes"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Mental Health Awareness Campaign"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Medical and dental missions"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Mental health awareness campaigns and counseling services"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "First aid training"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Fitness and wellness classes"
            End If
        End If
        
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Health and Wellness" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Nutrition Program"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Community Fitness Classes"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Mental Health Awareness Campaign"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Medical and dental missions"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Mental health awareness campaigns and counseling services"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "First aid training"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Fitness and wellness classes"
            End If
        End If

        '########################### Cultural Enhancement #################################
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Cultural Enhancement" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Community Arts Festival"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Cultural Festivals and Celebrations"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Traditional Arts and Crafts Workshops"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Historical Site Preservation Projects"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Cultural Competency Training"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Intercultural Dialogue Workshops"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Historical site preservation and restoration efforts"
            End If
        End If
        
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Cultural Enhancement" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Folk dance and music classes"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Historical site preservation and restoration efforts"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Language revitalization programs"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Community theater productions"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Intercultural Dialogue Workshops"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Language revitalization programs"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Historical site preservation and restoration efforts"
            End If
        End If
        
        '########################### Values Formation #################################
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Values Formation" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Values Education Curriculum"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Community Volunteer Corps"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Interfaith Dialogue Series"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Character education programs"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Youth leadership development workshops"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Anti-bullying campaigns"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Volunteerism initiatives"
            End If
        End If
        
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Values Formation" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Ethics seminars"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Community Volunteer Corps"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Interfaith Dialogue Series"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Basic Values Literacy Workshops"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Rediscovering Passion and Purpose Training"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Sharing Life Lessons and Values"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Sharing Life Lessons and Values"
            End If
        End If
        
        '########################### Disaster Management #################################
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Disaster Management" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Community Emergency Preparedness Workshops"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Search and Rescue Training"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Disaster Recovery and Rehabilitation Program"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Community-based disaster preparedness training"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Simulation exercises for disaster response drills"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Livelihood recovery programs post-disaster"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Psychological first aid training"
            End If
        End If
        
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Disaster Management" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Disaster risk reduction education"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Climate Change Adaptation Workshop"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "First Aid Training"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Flood/Earthquake/Fire Preparedness and Response Training"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Search and Rescue Simulation Exercise"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Hazard Identification and Risk Assessment Workshop"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Livestock and Agricultural Disaster Preparedness Training"
            End If
        End If
        
        '########################### Gender and Development #################################
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Gender and Development" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Safe Spaces for all gender"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Gender Engagement Program"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Gender sensitivity training"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Advocacy campaigns against gender-based violence"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Legal literacy seminars on gender rights and laws"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Gender-Based Violence Prevention and Response Workshop"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Gender-Responsive Parenting Workshops"
            End If
        End If
        
        If Cells(i, 2).Value = "25-34" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Gender and Development" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Orientation and Anti-Sexual and Safe Spaces"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Safe Spaces for all gender"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Gender Engagement Program"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Gender sensitivity training"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Kolehiyo" Then
                Cells(i, 16).Value = "Advocacy campaigns against gender-based violence"
            ElseIf Cells(i, 3).Value = "Kolehiyo" Then
                Cells(i, 16).Value = "Legal literacy seminars on gender rights and laws"
            ElseIf Cells(i, 3).Value = "Masters Degree" Then
                Cells(i, 16).Value = "Gender-Based Violence Prevention and Response Workshop"
            End If
        End If
    Next i
End Sub




