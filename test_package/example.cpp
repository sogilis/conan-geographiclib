#include <GeographicLib/Geodesic.hpp>
#include <iostream>

/**
 * This example is taken from GeographicLib documentation.
 * See https://geographiclib.sourceforge.io/html/start.html
 */
int main()
{
    const GeographicLib::Geodesic& geod = GeographicLib::Geodesic::WGS84();
    const double lat1 = 40.6;
    const double lon1 = -73.8;
    const double lat2 = 51.6;
    const double lon2 = -0.5;

    double s12;
    geod.Inverse(lat1, lon1, lat2, lon2, s12);
    std::cout << s12 / 1000 << " km\n";

    return 0;
}
