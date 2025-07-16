#include <zmq.hpp>
#include <iostream>
#include <string>
#include <vector>
#include "ecdsa_parser.h"
#include "stats_engine.h"

int main()
{
    zmq::context_t context(1);
    zmq::socket_t subscriber(context, ZMQ_SUB);

    const std::string connect_str = "tcp://bitcoind:28332"; // ZeroMQ dari bitcoind container
    subscriber.connect(connect_str);
    subscriber.setsockopt(ZMQ_SUBSCRIBE, "rawtx", 5);

    std::cout << "[C++ Daemon] Listening for rawtx on ZeroMQ..." << std::endl;

    while (true)
    {
        zmq::message_t message;
        subscriber.recv(&message);

        std::string raw_tx(static_cast<char *>(message.data()), message.size());
        std::vector<unsigned char> tx_data(raw_tx.begin(), raw_tx.end());

        std::vector<ECDSASignature> signatures = parse_signatures(tx_data);
        for (auto &sig : signatures)
        {
            update_stats(sig.r, sig.s);
            if (is_anomaly(sig.r, sig.s))
            {
                std::cout << "[!] Anomaly Detected: r=" << sig.r << ", s=" << sig.s << std::endl;
                // Kirim ke Python via gRPC atau file
            }
        }
    }

    return 0;
}