#-----------------------cargo

tbl_cargo = os.path.join(diretorio, 'Tabela Cargo.txt')
df_cargo= pd.read_csv(tbl_cargo, sep=';',encoding='latin-1',dtype=str)
df_cargo.to_sql( 'aux_cargo',engine,if_exists='replace',index=False)
print ('Tabela Cargo enviada')