import requests



import polyline
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap





def access_activity_data(access_token:str, params:dict=None) -> dict:
    from src.api_methods import endpoints
    headers:dict = {'Authorization': f'Bearer {access_token}'}
    print(headers)
    if not params:
        response:dict = requests.get(endpoints.activites_endpoint, headers=headers)
    else:
        response:dict = requests.get(endpoints.activites_endpoint, headers=headers, )
    response.raise_for_status()
    activity_data = response.json()
    # print(activity_data)
    for data in activity_data:
        coordinates = polyline.decode(data['map']['summary_polyline'])

        ride_longitudes = [coordinate[1] for coordinate in coordinates]
        ride_latitudes = [coordinate[0] for coordinate in coordinates]

        if 0:
            print(ride_longitudes[0], ride_latitudes[0] )

            ax = plt.subplot()

            m = Basemap(
                llcrnrlon=min(ride_longitudes) - 0.02,
                llcrnrlat=min(ride_latitudes) - 0.02,
                urcrnrlon=max(ride_longitudes) + 0.02,
                urcrnrlat=max(ride_latitudes) + 0.02,
                # epsg=23095,
                ax=ax
            )

            m.arcgisimage(xpixels=1000, verbose=True)
            # m.etopo()
            x, y = m(ride_longitudes, ride_latitudes)
            m.plot(x, y, 'r-')

            def on_ylims_change(event_ax):
                print("updated ylims: ", event_ax.get_ylim())
                x0, x1 = event_ax.get_xlim()
                y0, y1 = event_ax.get_ylim()

                # m = Basemap(
                #     llcrnrlon=x0,
                #     llcrnrlat=y0,
                #     urcrnrlon=x1,
                #     urcrnrlat=y1,
                #     # epsg=23095,
                # )

                m.arcgisimage(xpixels=1000, verbose=True)
                # m.etopo()
                x, y = m(ride_longitudes, ride_latitudes)
                m.plot(x, y, 'r-')




            ax.callbacks.connect('xlim_changed', on_ylims_change)
            ax.callbacks.connect('ylim_changed', on_ylims_change)

        else:
            plt.axes() .set_aspect('equal')
            plt.plot(ride_longitudes, ride_latitudes, )
        # plt.show()

    return activity_data


done = 0
x0 = 0
x1 = 0
y0 = 0
y1 = 0
call_x = 0
call_y = 0
if __name__ == "__main__":
    import pandas as pd
    datas = pd.read_csv('data\my_activity_data=20260228120007.csv')

    for data in datas.get('map.summary_polyline'):
        print(data)
        coordinates = polyline.decode(data)

        ride_longitudes = [coordinate[1] for coordinate in coordinates]
        ride_latitudes = [coordinate[0] for coordinate in coordinates]

        if 1:
            print(ride_longitudes[0], ride_latitudes[0] )

            ax = plt.subplot()

            m = Basemap(
                llcrnrlon=min(ride_longitudes) - 0.002,
                llcrnrlat=min(ride_latitudes) - 0.002,
                urcrnrlon=max(ride_longitudes) + 0.002,
                urcrnrlat=max(ride_latitudes) + 0.002,
                epsg=3395,
                projection='merc',
                ax=ax
            )

            m.arcgisimage(xpixels=400, verbose=True)
            # m.etopo()
            x, y = m(ride_longitudes, ride_latitudes)
            print(x[:3], ride_longitudes[:3])
            m.plot(ride_longitudes, ride_latitudes, 'r-', latlon = True)
            # m.imshow()


            def on_lims_change(event_ax, is_x):
                global done, call_x, call_y, m
                done = done + 1 if is_x else 2
                if done > 0 and done < 3:
                    pass
                    # plt.close()
                print(is_x)
                if is_x:
                    return
                print("updated ylims: ", event_ax.get_ylim())
                print("updated xlims: ", event_ax.get_xlim())
                # exit()
                x0, x1 = event_ax.get_xlim()
                y0, y1 = event_ax.get_ylim()

                # plt.close()
                # ax = plt.subplot()
                ax.callbacks.disconnect(call_x)
                ax.callbacks.disconnect(call_y)

                nx, ny = m([x0,x1], [y0, y1], inverse=True)
                ax.clear()
                m = Basemap(
                    llcrnrlon=nx[0],
                    llcrnrlat=ny[0],
                    urcrnrlon=nx[1],
                    urcrnrlat=ny[1],
                    ax=ax,
                    epsg=3395,
                    projection='merc',
                )
                try:
                    m.arcgisimage(xpixels=400, verbose=True)
                except:
                    pass
                # m.etopo()
                x, y = m(ride_longitudes, ride_latitudes)
                m.plot(ride_longitudes, ride_latitudes, 'r-', latlon = True)
                if done == 3:
                    pass
                call_x = ax.callbacks.connect('xlim_changed', on_xlims_change)
                call_y = ax.callbacks.connect('ylim_changed', on_ylims_change)
                plt.show()
                done = 0

            def on_xlims_change(event_ax):
                on_lims_change(event_ax, 1)

            def on_ylims_change(event_ax):
                on_lims_change(event_ax, 0)


            call_x = ax.callbacks.connect('xlim_changed', on_xlims_change)
            call_y = ax.callbacks.connect('ylim_changed', on_ylims_change)

        else:
            plt.axes() .set_aspect('equal')
            plt.plot(ride_longitudes, ride_latitudes, )
        plt.show()


    if 0:
        print(datas)
        m = Basemap(
                    llcrnrlat=40.361369, llcrnrlon=-80.0955278,
                    urcrnrlat=40.501368, urcrnrlon=-79.865723,
                    # epsg = 2272
                )
        m.arcgisimage( xpixels=700, verbose=True)
        plt.show()
