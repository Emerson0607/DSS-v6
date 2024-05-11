Sub Update_17_below()
    Dim lastRow As Long
    Dim i As Long
    
    ' Find the last row of data in column A
    lastRow = Cells(Rows.Count, "A").End(xlUp).Row
    
    ' Loop through each row
    For i = 1 To lastRow
        
        '########################### LITERACY #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Literacy" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Basic reading and writing workshops"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Digital Literacy for Beginners"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Life skills trainings"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Career Development Seminar"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Literacy" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Basic reading and writing workshops"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Creative Writing Workshops"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Digital Literacy for Beginners"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Vocational Training Workshop"
            End If
        End If
        
        '########################### Socio-economic #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Socio-economic" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Vocational Training Workshops"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Cooperative Development Initiatives"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Entrepreneurship Training"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Job Fairs and Career Counseling Sessions"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Socio-economic" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Entrepreneurship Bootcamp"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Financial Literacy seminars"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Vocational Training Workshops"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Job Fair and Skills Training Expo"
            End If
        End If
        
        '########################### Environmental Stewardship #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Environmental Stewardship" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Tree-Planting Campaign"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Urban Gardening Project"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Environmental Education Workshops"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Recycling and Waste Management Program"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Environmental Stewardship" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Sustainable Agriculture Practices Workshops"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Biodiversity Conservation Awareness Campaigns"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Community Gardens"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Zero Waste Lifestyle Workshop"
            End If
        End If
        
        '########################### Health and Wellness #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Health and Wellness" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Nutrition Basics Workshop"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Community Fitness Classes"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Mental Health Awareness Campaign"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Medical and Dental Missions"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Health and Wellness" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Mental health awareness campaigns and counseling services
"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "First Aid training"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Fitness and Wellness classes"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Stress Management Seminar"
            End If
        End If

        '########################### Cultural Enhancement #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Cultural Enhancement" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Community Arts Festival"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Traditional Arts and Crafts Workshops
"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Intercultural Dialogue Workshops"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Historical Site Preservation Projects"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Cultural Enhancement" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Folk dance and music classes"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Community theater productions featuring local stories"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Oral history projects"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Cultural exchange programs"
            End If
        End If
        
        '########################### Values Formation #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Values Formation" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Values Education"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Interfaith Dialogue Series"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Character education programs"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Youth leadership development workshops"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Values Formation" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Anti-bullying campaigns and peer support groups"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Volunteerism initiatives to instill a spirit of service"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Ethics seminars"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Civic engagement programs for youth empowerment"
            End If
        End If
        
        '########################### Disaster Management #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Disaster Management" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Community Emergency Preparedness Workshops"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Disaster Risk Mapping"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Search and Rescue Training"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Disaster Recovery and Rehabilitation Program"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Disaster Management" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Simulation exercises for disaster response drills"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Livelihood recovery programs post-disaster"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Psychological first aid training"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Disaster risk reduction education"
            End If
        End If
        
        '########################### Gender and Development #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Gender and Development" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Safe Spaces for all gender"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Gender Engagement Program"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Gender sensitivity training"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Advocacy campaigns against gender-based violence"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Gender and Development" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Legal literacy seminars on gender rights and laws"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Counseling and Mental Health Support
"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Gender-Based Violence Prevention and Response"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Gender empowerment workshops focusing on leadership and entrepreneurship"
            End If
        End If
    Next i
End Sub




