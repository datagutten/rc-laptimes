FROM debian:trixie AS build
ARG OPENSTINT_VERSION=master

RUN apt-get update && apt-get -y install build-essential cmake ninja-build git pkg-config libusb-1.0-0-dev libzmq3-dev cppzmq-dev libliquid-dev libfec-dev
RUN git clone https://github.com/zsellera/openstint --branch $OPENSTINT_VERSION --depth 1
WORKDIR /openstint
RUN cmake -G Ninja -DCMAKE_BUILD_TYPE=Release -B build .
RUN ninja -C build

FROM debian:trixie-slim
RUN apt-get update && apt-get -y install libusb-1.0.0-dev libzmq3-dev cppzmq-dev libliquid-dev libfec-dev && apt clean
COPY --from=build /openstint/build /openstint
COPY --from=build /openstint/integrations /openstint/integrations
CMD /openstint/src/openstint_rtlsdr -s /rc4 -t