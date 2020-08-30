import React, { useState, useEffect } from 'react';
import { Form } from 'formik';
import { Card, CardBody, Row, CardTitle, CardSubtitle, CardGroup } from 'reactstrap';
import { CustomCardHeader } from './Administration';
import { Icon, LoadingAnim, ErrorComponent, ParagraphTitle } from './UIElements';
import { Link } from 'react-router-dom';
import { Backend } from './DataManager';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faIdBadge } from '@fortawesome/free-solid-svg-icons';

const Home = (props) =>
(
  <div>
    "I'm Home"
  </div>
)

export default Home;


export const PublicHome = (props) => {
  const isSuperAdmin = props.isSuperAdmin;

  if (isSuperAdmin) {
    const [loading, setLoading] = useState(false);
    const [tenants, setTenants] = useState(null);
    const [error, setError] = useState(null);

    const backend = new Backend();

    useEffect(() => {
      setLoading(true);
      async function fetchData() {
        try {
          let json = await backend.fetchData('/api/v2/internal/public_tenants');
          let tenants_without_SP = []
          json.forEach(e => {
            if (e.name !== 'SuperPOEM Tenant')
              tenants_without_SP.push(e);
          })
          setTenants(tenants_without_SP);
        } catch(err) {
          setError(err);
        };
        setLoading(false);
      };
      fetchData();
    }, []);

    if (loading)
      return (<LoadingAnim/>);

    else if (error)
      return (<ErrorComponent error={error}/>);

    else if (!loading && tenants) {
      let groups = [];
      for (let i = 0; i < tenants.length; i = i + 3) {
        let cards = [];
        for (let j = 0; j < 3; j++) {
          if ((i + j) < tenants.length)
            cards.push(
              <Card className='mr-3' key={j + 1}>
                <CardTitle className='text-center'><h3>{tenants[i + j].name}</h3></CardTitle>
                <CardSubtitle className='mb-4 mt-3 text-center'>
                  <FontAwesomeIcon icon={faIdBadge} size='5x'/>
                </CardSubtitle>
                <CardBody>
                  <Card>
                    <CustomCardHeader title='Tenant resources'/>
                    <CardBody>
                      <Row className='p-1 align-items-center'>
                        <Icon i='metrics'/> <a href={`https://${tenants[i + j].domain_url}/ui/public_metrics`}>Metrics</a>
                      </Row>
                      <Row className='p-1 align-items-center'>
                        <Icon i='metricprofiles'/> <a href={`https://${tenants[i + j].domain_url}/ui/public_metricprofiles`}>Metric profiles</a>
                      </Row>
                      <Row className='p-1 align-items-center'>
                        <Icon i='aggregationprofiles'/> <a href={`https://${tenants[i + j].domain_url}/ui/public_aggregationprofiles`}>Aggregation profiles</a>
                      </Row>
                      <Row className='p-1 align-items-center'>
                        <Icon i='thresholdsprofiles'/> <a href={`https://${tenants[i + j].domain_url}/ui/public_thresholdsprofiles`}>Thresholds profiles</a>
                      </Row>
                      <Row className='p-1 align-items-center'>
                        <Icon i='operationsprofiles'/> <a href={`https://${tenants[i + j].domain_url}/ui/public_operationsprofiles`}>Operations profiles</a>
                      </Row>
                    </CardBody>
                  </Card>
                </CardBody>
              </Card>
            )
        }
        let group_width = '100%';
        if (cards.length == 1)
          group_width = '33.3333%';

        if (cards.length == 2)
          group_width = '66.6666%';

        groups.push(
          <CardGroup key={i} className='mb-3' style={{width: group_width}}>
            {
              cards.map((card, k) => card)
            }
          </CardGroup>
        )
      }
      return (
        <Form className='ml-2 mb-2 mt-2'>
          <h2 className='ml-3 mt-1 mb-4'>Public pages</h2>
          <Card className='mb-2'>
            <CustomCardHeader title='Shared resources'/>
            <CardBody>
              <Row className='p-1 align-items-center'>
                <Icon i='probes'/> <Link to={'/ui/public_probes'}>Probes</Link>
              </Row>
              <Row className='p-1 align-items-center'>
                <Icon i='metrictemplates'/> <Link to={'/ui/public_metrictemplates'}>Metric templates</Link>
              </Row>
            </CardBody>
          </Card>
          <ParagraphTitle title='Tenants'/>
          {
            groups.map((group, k) => group)
          }
        </Form>
      )
    } else
      return null;
  } else {
    return (
      <Form className='ml-2 mb-2 mt-2'>
        <h2 className='ml-3 mt-1 mb-4'>Public pages</h2>
        <Card className='mb-2'>
          <CustomCardHeader title='Shared resources'/>
          <CardBody>
            <Row className='p-1 align-items-center'>
              <Icon i='probes'/> <Link to={'/ui/public_probes'}>Probes</Link>
            </Row>
            <Row className='p-1 align-items-center'>
              <Icon i='metrictemplates'/> <Link to={'/ui/public_metrictemplates'}>Metric templates</Link>
            </Row>
          </CardBody>
        </Card>
        <Card className='mb-2'>
          <CustomCardHeader title='Tenant resources'/>
          <CardBody>
            <Row className='p-1 align-items-center'>
              <Icon i='metrics'/> <Link to={'/ui/public_metrics'}>Metrics</Link>
            </Row>
            <Row className='p-1 align-items-center'>
              <Icon i='metricprofiles'/> <Link to={'/ui/public_metricprofiles'}>Metric profiles</Link>
            </Row>
            <Row className='p-1 align-items-center'>
              <Icon i='aggregationprofiles'/> <Link to={'/ui/public_aggregationprofiles'}>Aggregation profiles</Link>
            </Row>
            <Row className='p-1 align-items-center'>
              <Icon i='thresholdsprofiles'/> <Link to={'/ui/public_thresholdsprofiles'}>Thresholds profiles</Link>
            </Row>
            <Row className='p-1 align-items-center'>
              <Icon i='operationsprofiles'/> <Link to={'/ui/public_operationsprofiles'}>Operations profiles</Link>
            </Row>
          </CardBody>
        </Card>
      </Form>
    );
  }
};
