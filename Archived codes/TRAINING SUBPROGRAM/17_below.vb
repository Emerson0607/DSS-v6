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
                Cells(i, 16).Value = "Socio Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Socio Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Socio Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Socio Kami4"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Socio-economic" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Socio Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Socio Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Socio Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Socio Kami4"
            End If
        End If
        
        '########################### Environmental Stewardship #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Environmental Stewardship" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Environmental Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Environmental Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Environmental Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Environmental Kami4"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Environmental Stewardship" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Environmental Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Environmental Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Environmental Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Environmental Kami4"
            End If
        End If
        
        '########################### Health and Wellness #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Health and Wellness" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Health Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Health Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Health Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Health Kami4"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Health and Wellness" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Health Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Health Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Health Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Health Kami4"
            End If
        End If

        '########################### Cultural Enhancement #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Cultural Enhancement" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Cultural Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Cultural Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Cultural KamI3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Cultural Kami4"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Cultural Enhancement" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Cultural Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Cultural Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Cultural Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Cultural Kami4"
            End If
        End If
        
        '########################### Values Formation #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Values Formation" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Values Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Values Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Values Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Values Kami4"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Values Formation" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Values Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Values Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Values Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Values Kami4"
            End If
        End If
        
        '########################### Disaster Management #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Disaster Management" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Disaster Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Disaster Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Disaster Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Disaster Kami4"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Disaster Management" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Disaster Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Disaster Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Disaster Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Disaster Kami4"
            End If
        End If
        
        '########################### Gender and Development #################################
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "May Trabaho" And Cells(i, 15).Value = "Gender and Development" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Gender Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Gender Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Gender Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Gender Kami4"
            End If
        End If
        
        If Cells(i, 2).Value = "17-below" And Cells(i, 4).Value = "Walang Trabaho" And Cells(i, 15).Value = "Gender and Development" Then
            If Cells(i, 3).Value = "Hindi nakapagtapos ng Elementarya" Then
                Cells(i, 16).Value = "Gender Kami1"
            ElseIf Cells(i, 3).Value = "Elementarya" Then
                Cells(i, 16).Value = "Gender Kami2"
            ElseIf Cells(i, 3).Value = "Hindi nakapagtapos ng Sekundarya" Then
                Cells(i, 16).Value = "Gender Kami3"
            ElseIf Cells(i, 3).Value = "Sekundarya" Then
                Cells(i, 16).Value = "Gender Kami4"
            End If
        End If
    Next i
End Sub




