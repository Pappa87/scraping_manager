INSERT INTO real_estate.real_estate_stage
(
	akadaly_mentes,
	alapterulet,
	ar,
	belmagassag,
	description,
	emelet,
	energiatanusitvany,
	epites_eve,
	epulet_szintjei,
	erkely,
	furdo_es_wc,
	futes,
	ingatlan_allapota,
	kertkapcsolatos,
	kilatas,
	komfort,
	lakopark_neve,
	legkondicionalo,
	lift,
	location,
	number_of_images,
	panelprogram,
	parkolas,
	parkolohely_ar,
	rezsikoltseg,
	szobak_szama,
	tajolas,
	tetoter,
	time_stamp,
	vasarlas_tipus,
	ID
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s), %s, %s)