@randomForest_Route.route("/programWithCSV2", methods=["GET", "POST"])
def programWithCSV2():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    if request.method == "POST":
        csv_file = request.files["csv_file"]
        
        if csv_file:
            df = pd.read_csv(csv_file)
            df = df.iloc[:, 3:]
            columns_with_strings = df.select_dtypes(include=['object']).columns

            sub_programs_dict = {
                "Literacy": db.session.query(Subprogram).filter(Subprogram.program == "Literacy").all(),
                "Socio-economic": db.session.query(Subprogram).filter(Subprogram.program == "Socio-economic").all(),
                "Environmental Stewardship": db.session.query(Subprogram).filter(Subprogram.program == "Environmental Stewardship").all(),
                "Health and Wellness": db.session.query(Subprogram).filter(Subprogram.program == "Health and Wellness").all(),
                "Cultural Enhancement": db.session.query(Subprogram).filter(Subprogram.program == "Cultural Enhancement").all(),
                "Values Formation": db.session.query(Subprogram).filter(Subprogram.program == "Values Formation").all(),
                "Disaster Management": db.session.query(Subprogram).filter(Subprogram.program == "Disaster Management").all(),
                "Gender and Development": db.session.query(Subprogram).filter(Subprogram.program == "Gender and Development").all()
            }
            db.session.close()

            if not columns_with_strings.empty:
                encoding_dict_kasarian = {'Lalake': 0, 'Babae': 1}
                encoding_dict_edad = {'17-below': 0, '18-24': 1, '25-34': 2, '35-44': 3, '45-54': 4, '55-64': 5, '65-Above': 6}
                encoding_dict_antas = {'Hindi nakapagtapos ng Elementarya':0, 'Elementarya':1, 'Hindi nakapagtapos ng Sekundarya':2, 'Sekundarya':3, 'Kolehiyo':4, 'Hindi nakapagtapos ng Kolehiyo':5, 'Masters Degree':6, 'Doctorate Degree':7, 'Hindi nakapag-aral':8}
                encoding_dict_uri = {'May Trabaho': 1, 'Walang Trabaho': 0}

                endcoding_dict_Pangedukasyon = {'Oo':1, 'Hindi': 0}
                endcoding_dict_Pangkultura = {'Oo':1, 'Hindi': 0}
                endcoding_dict_Pangkabuhayan = {'Oo':1, 'Hindi': 0}
                endcoding_dict_Values = {'Oo':1, 'Hindi': 0}
                endcoding_dict_Pagtatanim = {'Oo':1, 'Hindi': 0}
                endcoding_dict_Pagkain = {'Oo':1, 'Hindi': 0}
                endcoding_dict_Pangkalusugan = {'Oo':1, 'Hindi': 0}
                endcoding_dict_Pagrerecycle = {'Oo':1, 'Hindi': 0}
                endcoding_dict_Dental = {'Oo':1, 'Hindi': 0}
                endcoding_dict_Teknolohiya = {'Oo':1, 'Hindi': 0}

                df['Kasarian'] = df['Kasarian'].map(encoding_dict_kasarian)
                df['Edad'] = df['Edad'].map(encoding_dict_edad)
                df['Antas na tinapos'] = df['Antas na tinapos'].map(encoding_dict_antas)
                df['Uri ng trabaho'] = df['Uri ng trabaho'].map(encoding_dict_uri)
                df['Serbisyong Pangedukasyon'] = df['Serbisyong Pangedukasyon'].map(endcoding_dict_Pangedukasyon)
                df['Pagsasanay Pangkabuhayan (Livelihood)'] = df['Pagsasanay Pangkabuhayan (Livelihood)'].map(endcoding_dict_Pangkabuhayan)
                df['Pagtatanim'] = df['Pagtatanim'].map(endcoding_dict_Pagtatanim)
                df['Serbisyong Pangkalusugan'] = df['Serbisyong Pangkalusugan'].map(endcoding_dict_Pangkalusugan)
                df['Serbisyong Dental'] = df['Serbisyong Dental'].map(endcoding_dict_Dental)
                df['Kaalamang Pangkultura'] = df['Kaalamang Pangkultura'].map(endcoding_dict_Pangkultura)
                df['Values Formation at Moral Recovery'] = df['Values Formation at Moral Recovery'].map(endcoding_dict_Values)
                df['Ayudang Pagkain (Food Assistance)'] = df['Ayudang Pagkain (Food Assistance)'].map(endcoding_dict_Pagkain)
                df['Pagrerecycle'] = df['Pagrerecycle'].map(endcoding_dict_Pagrerecycle)
                df['Pagsasanay Ukol sa Teknolohiya'] = df['Pagsasanay Ukol sa Teknolohiya'].map(endcoding_dict_Teknolohiya)
                

            if "Program" in df.columns:
                target_variable = "Program"
                X = df.drop(target_variable, axis=1)
                predictions = model.predict(X)
                df["Predictions"] = predictions

            else:
                predictions = model.predict(df)
                df["Predictions"] = predictions

            prediction_counts = Counter(predictions)

            # Find the top 3 most frequent predictions
            top_3_predictions = prediction_counts.most_common(3)

             # Pass the top programs and their sub-programs to the template
            top_programs_with_subprograms = []
            for prediction, count in top_3_predictions:
                top_programs_with_subprograms.append({
                    "program": prediction,
                    "quantity": count,
                    "sub_programs": [sub_program.subprogram for sub_program in sub_programs_dict.get(prediction, [])]
            })
                
            kasarian_counts = df['Kasarian'].value_counts().to_dict()  
            edad_counts = df['Edad'].value_counts().to_dict()  
            antas_counts = df['Antas na tinapos'].value_counts().to_dict()  
            uri_counts = df['Uri ng trabaho'].value_counts().to_dict()  

            Pangedukasyon_counts = df['Serbisyong Pangedukasyon'].value_counts().to_dict()  
            Pangkabuhayan_counts = df['Pagsasanay Pangkabuhayan (Livelihood)'].value_counts().to_dict()  
            Pagtatanim_counts = df['Pagtatanim'].value_counts().to_dict()  
            Pangkalusugan_counts = df['Serbisyong Pangkalusugan'].value_counts().to_dict()  
            Dental_counts = df['Serbisyong Dental'].value_counts().to_dict()
            Pangkultura_counts = df['Kaalamang Pangkultura'].value_counts().to_dict()  
            Values_counts = df['Values Formation at Moral Recovery'].value_counts().to_dict()  
            Pagkain_counts = df['Ayudang Pagkain (Food Assistance)'].value_counts().to_dict()  
            Pagrerecycle_counts = df['Pagrerecycle'].value_counts().to_dict()  
            Teknolohiya_counts = df['Pagsasanay Ukol sa Teknolohiya'].value_counts().to_dict()  

            #highest count 
            # Define a dictionary with category counts
            category_counts = {
                "Pangedukasyon": Pangedukasyon_counts.get(1, 0),
                "Pangkabuhayan": Pangkabuhayan_counts.get(1, 0),
                "Pagtatanim": Pagtatanim_counts.get(1, 0),
                "Pangkalusugan": Pangkalusugan_counts.get(1, 0),
                "Dental": Dental_counts.get(1, 0),
                "Pangkultura": Pangkultura_counts.get(1, 0),
                "Values": Values_counts.get(1, 0),
                "Pagkain": Pagkain_counts.get(1, 0),
                "Pagrerecycle": Pagrerecycle_counts.get(1, 0),
                "Teknolohiya": Teknolohiya_counts.get(1, 0)
            }

            # Find the category with the highest count
            max_category = max(category_counts, key=category_counts.get)
            highest_count = category_counts[max_category]

            if max_category == "Pangedukasyon" or max_category == "Teknolohiya":
                program_ces = "Literacy"
            elif max_category == "Pangkabuhayan":
                program_ces = "Socio-economic"
            elif max_category == "Pagtatanim" or max_category == "Pagrerecycle":
                program_ces = "Environmental Stewardship"
            elif max_category == "Pangkalusugan" or max_category == "Dental":
                program_ces = "Health and Wellness"
            elif max_category == "Pangkultura":
                program_ces = "Cultural Enhancement"
            elif max_category == "Values":
                program_ces = "Values Formation"
            elif max_category == "Pagkain":
                program_ces = "Disaster Management"   
            else:
                program_ces = "Gender Development"  

            return render_template("resultCSV.html",
                top1=top_programs_with_subprograms[0] if len(top_programs_with_subprograms) >= 1 else {},
                top2=top_programs_with_subprograms[1] if len(top_programs_with_subprograms) >= 2 else {},
                top3=top_programs_with_subprograms[2] if len(top_programs_with_subprograms) >= 3 else {},
                kasarian_counts=kasarian_counts,
                edad_counts=edad_counts,
                antas_counts=antas_counts,
                uri_counts=uri_counts,
                Pangedukasyon_counts=Pangedukasyon_counts,
                Pangkabuhayan_counts=Pangkabuhayan_counts,
                Pagtatanim_counts=Pagtatanim_counts,
                Pangkalusugan_counts=Pangkalusugan_counts,
                Dental_counts=Dental_counts,
                Pangkultura_counts=Pangkultura_counts,
                Values_counts=Values_counts,
                Pagkain_counts=Pagkain_counts,
                Pagrerecycle_counts=Pagrerecycle_counts,
                Teknolohiya_counts=Teknolohiya_counts,
                max_category = max_category,
                highest_count=highest_count,
                program_ces = program_ces)
        
    return render_template("program.html")