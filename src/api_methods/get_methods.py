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

        if 1:
            print(ride_longitudes[0], ride_latitudes[0] )

            _, ax = plt.subplot()
           
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
            m.imshow()

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
        plt.show()

    return activity_data


done = 0
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
                llcrnrlon=min(ride_longitudes) - 0.02,
                llcrnrlat=min(ride_latitudes) - 0.02,
                urcrnrlon=max(ride_longitudes) + 0.02, 
                urcrnrlat=max(ride_latitudes) + 0.02,
                # epsg=23095,
                ax=ax
            )

            m.arcgisimage(xpixels=400, verbose=True)
            # m.etopo()
            x, y = m(ride_longitudes, ride_latitudes)
            m.plot(x, y, 'r-')
            # m.imshow()
            

            def on_lims_change(event_ax, is_x):
                global done
                done = done + 1 if is_x else 2
                if done > 0 and done < 3:
                    pass
                    # plt.close()

                print("updated ylims: ", event_ax.get_ylim())
                print("updated xlims: ", event_ax.get_xlim())
                x0, x1 = event_ax.get_xlim()
                y0, y1 = event_ax.get_ylim()
                
                plt.close()
                ax = plt.subplot()
                m = Basemap(
                    llcrnrlon=x0,
                    llcrnrlat=y0,
                    urcrnrlon=x1, 
                    urcrnrlat=y1,
                    ax=ax
                    # epsg=23095,
                )

                m.arcgisimage(xpixels=400, verbose=True)
                # m.etopo()
                x, y = m(ride_longitudes, ride_latitudes)
                m.plot(x, y, 'r-')
                if done == 3:
                    pass
                ax.callbacks.connect('xlim_changed', on_ylims_change)
                ax.callbacks.connect('ylim_changed', on_ylims_change)
                plt.show()
                done = 0
                
            def on_xlims_change(event_ax):
                on_lims_change(event_ax, 1)

            def on_ylims_change(event_ax):
                on_lims_change(event_ax, 0)
            
           
            ax.callbacks.connect('xlim_changed', on_xlims_change)
            ax.callbacks.connect('ylim_changed', on_ylims_change)

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