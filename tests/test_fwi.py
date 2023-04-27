# import matplotlib.pyplot as plt

from w31.back.fwi import FWIClass


def test_fwi():
    infile = open("tests/data.txt", "r")
    outfile = open("tests/fwioutput.txt", "w")

    infile.readline().rstrip()  # cut the header

    first_day = float(
        000.000
    )  # this need later to check if the day is the first day of collecting data

    sidekick = sorted(
        infile, key=lambda line: line.split()[1].split()[0]
    )  # file sorting by area and date

    error_list = []

    ffmc0, dmc0, dc0 = (
        None,
        None,
        None,
    )  # avoiding flake8 error "F821 undefined name 'ffmc'" and so on

    try:
        for line in sidekick:
            date, area, temp, rhum, wind, prcp, ffmc, dmc, dc, bui, isi, fwi = [
                float(field)
                for field in line.replace("bis", "999")
                .strip()
                .lstrip("[")
                .rstrip("]")
                .split()
            ]
            if rhum > 100.0:
                rhum = 100.0

            mth = int(str(date)[4:6])  # month extraction
            wind = wind * 3.6  # from m/s to km/h

            if first_day == area:

                fwisystem = FWIClass(temp, rhum, wind, prcp)

                ffmc_calc = fwisystem.FFMCcalc(ffmc0)
                dmc_calc = fwisystem.DMCcalc(dmc0, mth)
                dc_calc = fwisystem.DCcalc(dc0, mth)
                isi_calc = fwisystem.ISIcalc(ffmc_calc)
                bui_calc = fwisystem.BUIcalc(dmc_calc, dc_calc)
                fwi_calc = fwisystem.FWIcalc(isi_calc, bui_calc)

                ffmc0 = ffmc_calc
                dmc0 = dmc_calc
                dc0 = dc_calc

                error = fwi - fwi_calc

                error_list.append(error)

                outfile.write(
                    "%s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\n"
                    % (
                        ("data: " + str(date)),
                        ("area: " + str(area)),
                        ("temp: " + str(round(temp, 4))),
                        ("rhum: " + str(round(rhum, 4))),
                        ("wind: " + str(round(wind, 4))),
                        ("prcp: " + str(round(prcp, 4))),
                        ("ffmc: " + str(round(ffmc_calc, 4))),
                        ("dmc: " + str(round(dmc_calc, 4))),
                        ("dc: " + str(round(dc_calc, 4))),
                        ("isi: " + str(round(isi_calc, 4))),
                        ("bui: " + str(round(bui_calc, 4))),
                        ("fwi: " + str(round(fwi_calc, 4))),
                        ("error: " + str(error)),
                    )
                )

                # assert abs(error) <= 0.8

            else:
                ffmc0 = ffmc
                dmc0 = dmc
                dc0 = dc

                outfile.write(
                    "%s\t %s\t %s\t %s\t %s\t %s\n"
                    % (
                        ("data: " + str(date)),
                        ("area: " + str(area)),
                        ("temp: " + str(round(temp, 4))),
                        ("rhum: " + str(round(rhum, 4))),
                        ("wind: " + str(round(wind, 4))),
                        ("prcp: " + str(round(prcp, 4))),
                    )
                )
                first_day = area

    finally:
        infile.close()
        outfile.close()

    # # plot of the fwi delta error
    # fig = plt.figure()
    # plt.plot(error_list)
    # plt.title("Δ error")
    # fig.savefig("tests/fwi_delta_error")


if __name__ == "__main__":
    test_fwi()
